#!/usr/bin/env bash
# Integration test script for E2B
# Tests all components together to ensure seamless integration

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

TEST_RESULTS_DIR="/tmp/e2b_integration_tests"
FAILED_TESTS=0
PASSED_TESTS=0

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

test_agentx5_basic() {
    log_info "Testing AgentX5 basic functionality..."
    
    cd "$PROJECT_ROOT/tools/agentx5"
    
    if python3 multi_dump_parser.py example_dump.txt "$TEST_RESULTS_DIR/agentx5_output" &>/dev/null; then
        log_success "AgentX5 basic test passed"
        ((PASSED_TESTS++))
        return 0
    else
        log_error "AgentX5 basic test failed"
        ((FAILED_TESTS++))
        return 1
    fi
}

test_agentx5_unit_tests() {
    log_info "Testing AgentX5 unit tests..."
    
    cd "$PROJECT_ROOT/tools/agentx5"
    
    if pytest -q test_multi_dump_parser.py &>/dev/null; then
        log_success "AgentX5 unit tests passed"
        ((PASSED_TESTS++))
        return 0
    else
        log_error "AgentX5 unit tests failed"
        ((FAILED_TESTS++))
        return 1
    fi
}

test_build_scripts() {
    log_info "Testing build scripts..."
    
    cd "$PROJECT_ROOT"
    
    if ./scripts/build.sh --target agentx5 &>/dev/null; then
        log_success "Build script test passed"
        ((PASSED_TESTS++))
        return 0
    else
        log_error "Build script test failed"
        ((FAILED_TESTS++))
        return 1
    fi
}

test_validation_scripts() {
    log_info "Testing validation scripts..."
    
    cd "$PROJECT_ROOT"
    
    if ./scripts/validate.sh &>/dev/null; then
        log_success "Validation script test passed"
        ((PASSED_TESTS++))
        return 0
    else
        log_error "Validation script test failed"
        ((FAILED_TESTS++))
        return 1
    fi
}

test_api_consistency() {
    log_info "Testing API consistency..."
    
    cd "$PROJECT_ROOT"
    
    if python3 scripts/check_api_consistency.py &>/dev/null; then
        log_success "API consistency test passed"
        ((PASSED_TESTS++))
        return 0
    else
        log_error "API consistency test failed"
        ((FAILED_TESTS++))
        return 1
    fi
}

test_environment_parity() {
    log_info "Testing environment parity..."
    
    # Check if .env.template exists and has required variables
    if [ -f "$PROJECT_ROOT/.env.template" ]; then
        local required_vars=(
            "APP_NAME"
            "APP_ENVIRONMENT"
            "BUILD_TARGET"
            "SANDBOX_ENABLED"
        )
        
        local missing_vars=0
        for var in "${required_vars[@]}"; do
            if ! grep -q "$var" "$PROJECT_ROOT/.env.template"; then
                log_error "Missing environment variable: $var"
                ((missing_vars++))
            fi
        done
        
        if [ $missing_vars -eq 0 ]; then
            log_success "Environment parity test passed"
            ((PASSED_TESTS++))
            return 0
        else
            log_error "Environment parity test failed"
            ((FAILED_TESTS++))
            return 1
        fi
    else
        log_error ".env.template not found"
        ((FAILED_TESTS++))
        return 1
    fi
}

test_documentation() {
    log_info "Testing documentation completeness..."
    
    local docs=(
        "BUILD_DEPLOYMENT_GUIDE.md"
        "integration.yml"
        "README.md"
    )
    
    local missing_docs=0
    for doc in "${docs[@]}"; do
        if [ ! -f "$PROJECT_ROOT/$doc" ]; then
            log_error "Missing documentation: $doc"
            ((missing_docs++))
        fi
    done
    
    if [ $missing_docs -eq 0 ]; then
        log_success "Documentation test passed"
        ((PASSED_TESTS++))
        return 0
    else
        log_error "Documentation test failed"
        ((FAILED_TESTS++))
        return 1
    fi
}

generate_test_report() {
    log_info "Generating integration test report..."
    
    cat > "$PROJECT_ROOT/integration_test_report.txt" << EOF
E2B Integration Test Report
===========================
Date: $(date)

Total Tests: $((PASSED_TESTS + FAILED_TESTS))
Passed: $PASSED_TESTS
Failed: $FAILED_TESTS

Test Results:
$([ $FAILED_TESTS -eq 0 ] && echo "✓ All tests passed!" || echo "✗ Some tests failed")

Status: $([ $FAILED_TESTS -eq 0 ] && echo "SUCCESS" || echo "FAILURE")
EOF
    
    log_success "Test report generated: integration_test_report.txt"
}

cleanup() {
    log_info "Cleaning up test artifacts..."
    rm -rf "$TEST_RESULTS_DIR"
}

main() {
    log_info "Starting E2B integration tests..."
    echo ""
    
    # Create test results directory
    mkdir -p "$TEST_RESULTS_DIR"
    
    # Run all tests
    test_agentx5_basic || true
    test_agentx5_unit_tests || true
    test_build_scripts || true
    test_validation_scripts || true
    test_api_consistency || true
    test_environment_parity || true
    test_documentation || true
    
    echo ""
    generate_test_report
    echo ""
    
    cleanup
    
    # Display summary
    log_info "Test Summary:"
    log_info "  Passed: $PASSED_TESTS"
    log_info "  Failed: $FAILED_TESTS"
    echo ""
    
    if [ $FAILED_TESTS -eq 0 ]; then
        log_success "All integration tests passed!"
        exit 0
    else
        log_error "Integration tests completed with failures"
        exit 1
    fi
}

main
