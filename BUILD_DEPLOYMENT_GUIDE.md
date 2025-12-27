# E2B Build and Deployment Guide

## Overview

This guide provides comprehensive instructions for building, testing, and deploying the E2B project across different environments (sandbox and production).

## Table of Contents

- [Architecture](#architecture)
- [Environment Setup](#environment-setup)
- [Building the Project](#building-the-project)
- [Testing](#testing)
- [Deployment](#deployment)
- [Environment Parity](#environment-parity)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

## Architecture

E2B consists of multiple components:

- **JavaScript SDK** (`packages/js-sdk`): Core SDK for Node.js, Browser, Deno, and Bun
- **Python SDK** (`packages/python-sdk`): Python bindings for E2B
- **CLI** (`packages/cli`): Command-line interface for managing E2B sandboxes
- **AgentX5 Tool** (`tools/agentx5`): Data parsing and processing tool
- **Web Application** (`apps/web`): Documentation and web interface

## Environment Setup

### Prerequisites

- Node.js 20.19.5 or later
- pnpm 9.15.5 or later
- Python 3.9 or later
- Poetry 2.1.1 or later (for Python SDK)

### Installation

```bash
# Clone the repository
git clone https://github.com/APPSHOLDINGSWYINC/E2B.git
cd E2B

# Install dependencies
pnpm install --frozen-lockfile

# Install Python dependencies for AgentX5
cd tools/agentx5
pip install -r requirements.txt
```

## Building the Project

### Using the Build Script

The project includes a comprehensive build script that handles all components:

```bash
# Build all components
./scripts/build.sh

# Build specific components
./scripts/build.sh --target js-sdk
./scripts/build.sh --target cli
./scripts/build.sh --target python-sdk
./scripts/build.sh --target agentx5

# Build for specific environment
./scripts/build.sh --environment production
./scripts/build.sh --environment sandbox
```

### Manual Build Steps

#### JavaScript SDK

```bash
cd packages/js-sdk
pnpm build
```

#### CLI

```bash
cd packages/cli
pnpm build
```

#### Python SDK

```bash
cd packages/python-sdk
poetry build
```

#### AgentX5 Tool

AgentX5 doesn't require a build step, but you can validate it:

```bash
cd tools/agentx5
python -m py_compile multi_dump_parser.py
python multi_dump_parser.py example_dump.txt output/
```

## Testing

### Running All Tests

```bash
# Run all tests
pnpm test

# Run tests for specific component
cd packages/js-sdk && pnpm test
cd packages/cli && pnpm test
cd packages/python-sdk && poetry run pytest
cd tools/agentx5 && pytest -v
```

### Test Coverage

```bash
# Generate coverage report for AgentX5
cd tools/agentx5
pytest --cov=multi_dump_parser --cov-report=html
```

### Test Types

- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test full workflows

## Deployment

### Validation Before Deployment

Always validate your deployment before pushing to production:

```bash
./scripts/validate.sh
```

This checks:
- Environment parity between sandbox and production
- Build artifacts
- Test infrastructure
- CI/CD workflows
- API consistency

### Environment Configuration

Copy the environment template and configure for your environment:

```bash
cp .env.template .env

# Edit .env with your configuration
# For production:
ENVIRONMENT=production
BUILD_TARGET=all

# For sandbox:
ENVIRONMENT=sandbox
SANDBOX_MIRROR_PRODUCTION=true
```

### Deployment Checklist

- [ ] All tests pass locally
- [ ] Code has been linted and formatted
- [ ] Build artifacts are up to date
- [ ] Environment variables are configured
- [ ] Validation script passes
- [ ] CI/CD workflows pass
- [ ] Security scans pass

## Environment Parity

E2B ensures parity between sandbox and production environments through:

### Configuration Management

- All environment-specific settings are in `.env` files
- `.env.template` provides a baseline configuration
- Environment variables control behavior across environments

### Build Process

- Same build scripts work in both environments
- Build artifacts are identical
- Dependencies are locked via `pnpm-lock.yaml` and `poetry.lock`

### Testing

- Same test suites run in both environments
- Test data is consistent
- Test coverage requirements are identical

## CI/CD Integration

### GitHub Actions Workflows

The project uses GitHub Actions for continuous integration:

- **`js_sdk_tests.yml`**: Tests JavaScript SDK on multiple platforms
- **`python_sdk_tests.yml`**: Tests Python SDK
- **`cli_tests.yml`**: Tests CLI functionality
- **`agentx5_tests.yml`**: Tests AgentX5 tool
- **`lint.yml`**: Runs linters across the codebase

### Workflow Triggers

Workflows are triggered on:
- Pull requests to `main`
- Pushes to `main`
- Manual workflow dispatch

### Secrets Required

- `E2B_API_KEY`: Required for SDK integration tests

## Troubleshooting

### Build Failures

**Problem**: `pnpm install` fails
```bash
# Solution: Clear cache and reinstall
pnpm store prune
rm -rf node_modules
pnpm install --frozen-lockfile
```

**Problem**: Python dependencies fail to install
```bash
# Solution: Upgrade pip and retry
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Test Failures

**Problem**: E2B API tests fail
```bash
# Solution: Check API key is set
echo $E2B_API_KEY
# If not set, create one at https://e2b.dev/dashboard?tab=keys
export E2B_API_KEY=your_key_here
```

**Problem**: AgentX5 tests fail
```bash
# Solution: Ensure pandas is installed
pip install pandas pytest pytest-cov
pytest -v
```

### CI/CD Issues

**Problem**: Workflow requires approval
- Check repository settings for workflow permissions
- Ensure actions have read/write permissions

**Problem**: Workflow fails on specific OS
- Check OS-specific dependencies in workflow file
- Test locally on the same OS if possible

## Best Practices

### Development

1. Always run tests before committing
2. Use the build script for consistency
3. Keep dependencies up to date
4. Follow the existing code style

### Testing

1. Write tests for new features
2. Maintain test coverage above 80%
3. Test on multiple platforms when possible
4. Use meaningful test names

### Deployment

1. Always validate before deploying
2. Deploy to sandbox first
3. Monitor for errors after deployment
4. Keep rollback plan ready

## Additional Resources

- [E2B Documentation](https://e2b.dev/docs)
- [GitHub Repository](https://github.com/APPSHOLDINGSWYINC/E2B)
- [E2B Cookbook](https://github.com/e2b-dev/e2b-cookbook)

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review CI/CD logs for errors
