# GitLab CI/CD Setup Guide

This document provides comprehensive instructions for setting up continuous deployment in GitLab for the E2B project.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Using Auto DevOps](#using-auto-devops)
3. [Manual CI/CD Pipeline Configuration](#manual-cicd-pipeline-configuration)
4. [Deployment Strategies](#deployment-strategies)
5. [Environment Variables](#environment-variables)
6. [Admin-Level Configuration](#admin-level-configuration)

## Prerequisites

Before setting up GitLab CI/CD, ensure you have:

- A GitLab account with appropriate permissions for your project
- GitLab Runner configured and registered for your project
- Access to set CI/CD variables in your GitLab project settings
- Required secrets and tokens (E2B_API_KEY, NPM_TOKEN, PYPI_TOKEN, etc.)

## Using Auto DevOps

Auto DevOps provides an automated continuous deployment solution that requires minimal configuration.

### Enabling Auto DevOps

1. **Navigate to your project** in GitLab
2. Go to **Settings** > **CI/CD**
3. Expand the **Auto DevOps** section
4. Check **Default to Auto DevOps pipeline**
5. Click **Save changes**

> **Note:** Auto DevOps runs automatically for projects without a `.gitlab-ci.yml` file. If you have a `.gitlab-ci.yml` file, Auto DevOps will be disabled.

### Deployment Strategies with Auto DevOps

#### Continuous Deployment to Production

To enable continuous deployment where every commit to the default branch is automatically deployed to production:

1. Go to **Settings** > **CI/CD** > **Variables**
2. Add a new variable:
   - **Key:** `CONTINUOUS_DEPLOYMENT`
   - **Value:** `true`
   - **Protected:** Yes (recommended)
   - **Masked:** No

#### Continuous Deployment with Timed Incremental Rollout

For continuous deployment with a 5-minute delay between rollouts:

1. Go to **Settings** > **CI/CD** > **Variables**
2. Add two variables:
   - **Variable 1:**
     - **Key:** `CONTINUOUS_DEPLOYMENT`
     - **Value:** `true`
     - **Protected:** Yes
   - **Variable 2:**
     - **Key:** `INCREMENTAL_ROLLOUT_MODE`
     - **Value:** `timed`
     - **Protected:** Yes

### Auto DevOps Prerequisites

Before enabling Auto DevOps:

1. **Set the base domain:**
   - Go to **Settings** > **CI/CD** > **Auto DevOps**
   - Enter your base domain (e.g., `example.com`)
   - This allows GitLab to automatically create review apps and deploy environments

2. **Configure Kubernetes cluster** (if using Kubernetes):
   - Go to **Infrastructure** > **Kubernetes clusters**
   - Add a cluster or connect an existing one
   - Ensure the cluster has sufficient resources

## Manual CI/CD Pipeline Configuration

The E2B project includes a comprehensive `.gitlab-ci.yml` file that provides more control over the CI/CD process.

### Pipeline Structure

The pipeline consists of the following stages:

```yaml
stages:
  - setup      # Install dependencies and validate environment
  - lint       # Run linting checks
  - test       # Run all test suites
  - build      # Build packages and applications
  - deploy     # Deploy to staging/production
```

### Key Features

- **Multi-language support:** Handles Node.js (JavaScript/TypeScript) and Python packages
- **Parallel testing:** Runs JS SDK, Python SDK, and CLI tests in parallel
- **Artifact management:** Preserves build artifacts for deployment
- **Environment-specific deployments:** Separate jobs for staging and production
- **Flexible deployment modes:** Manual, continuous, or timed incremental rollout

### Customizing the Pipeline

#### Modifying Stages

Edit `.gitlab-ci.yml` to add, remove, or reorder stages:

```yaml
stages:
  - setup
  - lint
  - test
  - security-scan  # Add a new stage
  - build
  - deploy
```

#### Adding New Jobs

Add a new job under the appropriate stage:

```yaml
security-scan:
  stage: security-scan
  script:
    - pnpm audit
    - pnpm run security-check
  only:
    - main
    - merge_requests
```

#### Configuring Dependencies

Use `needs` to control job dependencies:

```yaml
deploy:production:
  needs:
    - build:web
    - build:packages
    - test:js-sdk
    - test:python-sdk
```

## Deployment Strategies

### Strategy 1: Manual Deployment (Default)

By default, production deployments require manual approval:

```yaml
deploy:production:manual:
  when: manual
```

To deploy:
1. Go to **CI/CD** > **Pipelines**
2. Click on the pipeline for your commit
3. Find the `deploy:production:manual` job
4. Click the **Play** button

### Strategy 2: Continuous Deployment

Enable automatic deployment to production on every commit to `main`:

1. Set the `CONTINUOUS_DEPLOYMENT` variable to `true`
2. Commits to `main` will automatically deploy to production

### Strategy 3: Timed Incremental Rollout

Enable continuous deployment with a 5-minute delay between rollouts:

1. Set `CONTINUOUS_DEPLOYMENT` to `true`
2. Set `INCREMENTAL_ROLLOUT_MODE` to `timed`
3. Each deployment will wait 5 minutes before proceeding

This strategy is useful for:
- Gradual rollouts to minimize risk
- Monitoring deployments before full rollout
- Allowing time for automated health checks

### Strategy 4: Staging-First Deployment

Deploy to staging first, then manually promote to production:

1. Merge to `develop` branch → Automatic deployment to staging
2. Merge to `main` branch → Manual deployment to production

## Environment Variables

### Required Variables

Set these variables in **Settings** > **CI/CD** > **Variables**:

| Variable | Description | Required | Protected | Masked |
|----------|-------------|----------|-----------|--------|
| `E2B_API_KEY` | E2B API authentication key | Yes | Yes | Yes |
| `NPM_TOKEN` | NPM registry authentication token | For npm publish | Yes | Yes |
| `PYPI_TOKEN` | PyPI authentication token | For PyPI publish | Yes | Yes |

### Optional Variables

| Variable | Description | Default | Values |
|----------|-------------|---------|--------|
| `CONTINUOUS_DEPLOYMENT` | Enable continuous deployment | `false` | `true`, `false` |
| `INCREMENTAL_ROLLOUT_MODE` | Rollout strategy | `manual` | `manual`, `timed` |
| `NODE_VERSION` | Node.js version | From `.tool-versions` | Any valid version |
| `PNPM_VERSION` | pnpm version | From `.tool-versions` | Any valid version |
| `PYTHON_VERSION` | Python version | From `.tool-versions` | Any valid version |

### Setting Variables

1. Navigate to your project in GitLab
2. Go to **Settings** > **CI/CD**
3. Expand **Variables**
4. Click **Add variable**
5. Enter the key and value
6. Configure protection and masking options:
   - **Protected:** Only available in protected branches (recommended for production secrets)
   - **Masked:** Hide value in job logs (recommended for sensitive data)
7. Click **Add variable**

## Admin-Level Configuration

For GitLab administrators managing instance-wide settings on self-managed GitLab instances:

### Accessing Admin Settings

1. Navigate to **Admin Area** (wrench icon in the top right)
2. Go to **Settings** > **CI/CD**
3. Expand **Continuous Integration and Deployment**

### Instance-Wide Auto DevOps

To enable Auto DevOps for all projects by default:

1. In **Admin** > **Settings** > **CI/CD**
2. Expand **Auto DevOps**
3. Check **Default to Auto DevOps pipeline for all projects**
4. Configure the **Auto DevOps base domain** (e.g., `example.com`)
5. Click **Save changes**

### Configuring Runners

Configure shared runners for all projects:

1. Go to **Admin** > **CI/CD** > **Runners**
2. Click **New instance runner**
3. Configure runner settings:
   - Platform (Linux, Windows, macOS)
   - Tags for specific job matching
   - Whether the runner is locked to the project
4. Follow the registration instructions

### Artifact Storage Settings

Configure artifact retention and storage:

1. In **Admin** > **Settings** > **CI/CD**
2. Expand **Continuous Integration and Deployment**
3. Set **Default artifacts expiration**
4. Configure **Maximum artifacts size**
5. Click **Save changes**

### Pipeline Settings

Configure pipeline behavior:

1. Set **Default Git clone method** (shallow, full)
2. Configure **Git strategy** (fetch, clone)
3. Set **Default pipeline timeout**
4. Enable/disable **Auto-cancel redundant pipelines**

## Monitoring and Debugging

### Viewing Pipeline Status

1. Go to **CI/CD** > **Pipelines**
2. Click on a pipeline to view job details
3. Click on a job to view logs

### Common Issues and Solutions

#### Issue: Dependencies not installing

**Solution:** Clear the cache and retry:
1. Go to **CI/CD** > **Pipelines**
2. Click **Clear runner caches**
3. Rerun the pipeline

#### Issue: Deployment fails with authentication error

**Solution:** Verify that all required variables are set:
1. Go to **Settings** > **CI/CD** > **Variables**
2. Ensure `E2B_API_KEY`, `NPM_TOKEN`, and `PYPI_TOKEN` are set
3. Check that tokens are not expired

#### Issue: Pipeline takes too long

**Solution:** Enable parallel execution:
- Ensure multiple runners are available
- Use `needs` instead of `dependencies` to allow parallel jobs
- Consider increasing runner capacity

## Best Practices

1. **Use protected branches:** Configure `main` and `develop` as protected branches
2. **Require merge request approvals:** Enable approval rules for production deployments
3. **Use environments:** Define clear environments (staging, production) in `.gitlab-ci.yml`
4. **Monitor deployments:** Set up alerts and monitoring for production deployments
5. **Test in staging first:** Always test changes in staging before production
6. **Version your deployments:** Use Git tags for release versions
7. **Keep secrets secure:** Always mark sensitive variables as masked and protected

## Additional Resources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Auto DevOps Guide](https://docs.gitlab.com/ee/topics/autodevops/)
- [GitLab Runner Installation](https://docs.gitlab.com/runner/install/)
- [Pipeline Configuration Reference](https://docs.gitlab.com/ee/ci/yaml/)
