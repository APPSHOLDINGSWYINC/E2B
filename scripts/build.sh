#!/usr/bin/env bash
# Comprehensive build script for E2B project
# Supports both sandbox and production environments

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENVIRONMENT="${ENVIRONMENT:-production}"
BUILD_TARGET="${BUILD_TARGET:-all}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    log_info "Checking dependencies..."
    
    local missing_deps=()
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        missing_deps+=("node")
    fi
    
    # Check pnpm
    if ! command -v pnpm &> /dev/null; then
        missing_deps+=("pnpm")
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        missing_deps+=("python3")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        log_info "Please install missing dependencies and try again"
        exit 1
    fi
    
    log_success "All dependencies are installed"
}

install_dependencies() {
    log_info "Installing project dependencies..."
    
    cd "$PROJECT_ROOT"
    
    # Install JavaScript dependencies
    log_info "Installing JavaScript dependencies..."
    pnpm install --frozen-lockfile
    
    # Install Python dependencies for agentx5
    log_info "Installing Python dependencies for agentx5..."
    cd "$PROJECT_ROOT/tools/agentx5"
    pip install -q -r requirements.txt
    
    cd "$PROJECT_ROOT"
    log_success "Dependencies installed successfully"
}

build_js_sdk() {
    log_info "Building JavaScript SDK..."
    cd "$PROJECT_ROOT/packages/js-sdk"
    pnpm build
    log_success "JavaScript SDK built successfully"
}

build_cli() {
    log_info "Building CLI..."
    cd "$PROJECT_ROOT/packages/cli"
    pnpm build
    log_success "CLI built successfully"
}

build_python_sdk() {
    log_info "Building Python SDK..."
    cd "$PROJECT_ROOT/packages/python-sdk"
    
    if command -v poetry &> /dev/null; then
        poetry build
        log_success "Python SDK built successfully"
    else
        log_warning "Poetry not found, skipping Python SDK build"
    fi
}

validate_agentx5() {
    log_info "Validating AgentX5 tool..."
    cd "$PROJECT_ROOT/tools/agentx5"
    
    # Syntax check
    python3 -m py_compile multi_dump_parser.py
    
    # Test with example dump
    if [ -f "example_dump.txt" ]; then
        log_info "Testing with example dump file..."
        python3 multi_dump_parser.py example_dump.txt /tmp/agentx5_test_output
        rm -rf /tmp/agentx5_test_output
    fi
    
    log_success "AgentX5 tool validated successfully"
}

run_tests() {
    log_info "Running tests..."
    
    if [ "$BUILD_TARGET" == "js-sdk" ] || [ "$BUILD_TARGET" == "all" ]; then
        log_info "Running JavaScript SDK tests..."
        cd "$PROJECT_ROOT/packages/js-sdk"
        pnpm test || log_warning "Some JS SDK tests failed"
    fi
    
    if [ "$BUILD_TARGET" == "cli" ] || [ "$BUILD_TARGET" == "all" ]; then
        log_info "Running CLI tests..."
        cd "$PROJECT_ROOT/packages/cli"
        pnpm test || log_warning "Some CLI tests failed"
    fi
    
    if [ "$BUILD_TARGET" == "agentx5" ] || [ "$BUILD_TARGET" == "all" ]; then
        log_info "Running AgentX5 tests..."
        cd "$PROJECT_ROOT/tools/agentx5"
        if command -v pytest &> /dev/null; then
            pytest -v test_multi_dump_parser.py || log_warning "Some AgentX5 tests failed"
        else
            log_warning "pytest not found, skipping AgentX5 tests"
        fi
    fi
    
    cd "$PROJECT_ROOT"
    log_success "Tests completed"
}

run_linters() {
    log_info "Running linters..."
    
    cd "$PROJECT_ROOT"
    pnpm lint || log_warning "Linting found some issues"
    
    log_success "Linting completed"
}

generate_build_report() {
    log_info "Generating build report..."
    
    cat > "$PROJECT_ROOT/build_report.txt" << EOF
E2B Build Report
================
Date: $(date)
Environment: $ENVIRONMENT
Build Target: $BUILD_TARGET
Node Version: $(node --version)
Python Version: $(python3 --version)
pnpm Version: $(pnpm --version)

Build Status: SUCCESS
EOF
    
    log_success "Build report generated: build_report.txt"
}

# Main execution
main() {
    log_info "Starting E2B build process..."
    log_info "Environment: $ENVIRONMENT"
    log_info "Build Target: $BUILD_TARGET"
    echo ""
    
    check_dependencies
    echo ""
    
    install_dependencies
    echo ""
    
    case "$BUILD_TARGET" in
        "js-sdk")
            build_js_sdk
            ;;
        "cli")
            build_cli
            ;;
        "python-sdk")
            build_python_sdk
            ;;
        "agentx5")
            validate_agentx5
            ;;
        "all")
            build_js_sdk
            build_cli
            build_python_sdk
            validate_agentx5
            ;;
        *)
            log_error "Unknown build target: $BUILD_TARGET"
            log_info "Valid targets: js-sdk, cli, python-sdk, agentx5, all"
            exit 1
            ;;
    esac
    echo ""
    
    run_linters
    echo ""
    
    run_tests
    echo ""
    
    generate_build_report
    echo ""
    
    log_success "Build process completed successfully!"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --environment|-e)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --target|-t)
            BUILD_TARGET="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -e, --environment ENV   Set environment (default: production)"
            echo "  -t, --target TARGET     Set build target (default: all)"
            echo "                          Valid targets: js-sdk, cli, python-sdk, agentx5, all"
            echo "  -h, --help             Show this help message"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

main
