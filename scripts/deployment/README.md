# Deployment Scripts

This directory contains deployment scripts and configurations for the E2B project.

## Contents

- `deploy.sh` - Main deployment script
- Environment configuration examples (`.env.staging.example`, `.env.production.example`)

## Quick Start

### 1. Configure Environment Variables

Create environment-specific configuration files:

```bash
# For staging
cp .env.staging.example .env.staging
# Edit .env.staging and fill in the actual values

# For production
cp .env.production.example .env.production
# Edit .env.production and fill in the actual values
```

### 2. Run Deployment

```bash
# Deploy to staging (full deployment)
./scripts/deployment/deploy.sh staging full

# Deploy to production (full deployment)
./scripts/deployment/deploy.sh production full

# Deploy only packages
./scripts/deployment/deploy.sh staging packages

# Deploy only web app
./scripts/deployment/deploy.sh staging web
```

## Deployment Types

- **full** - Deploys all packages and the web application
- **packages** - Deploys only the SDK packages (JS, Python, CLI)
- **web** - Deploys only the web application

## Customizing the Deployment Script

The `deploy.sh` script is a template that you should customize for your specific deployment needs. Add your deployment commands in the appropriate sections:

### For Staging Deployments

Add commands after this line in `deploy.sh`:
```bash
# Add your staging deployment commands here
```

Examples:
- SSH deployment: `ssh user@staging-server "cd /app && git pull && pnpm install && pnpm run build"`
- Cloud platform: `gcloud app deploy --project=e2b-staging`
- Container deployment: `docker build -t e2b-staging . && docker push e2b-staging`

### For Production Deployments

Add commands after this line in `deploy.sh`:
```bash
# Add your production deployment commands here
```

Examples:
- Vercel: `vercel deploy --prod`
- AWS: `aws s3 sync ./dist s3://your-bucket --delete`
- Kubernetes: `kubectl apply -f k8s/production/`

## GitLab CI/CD Integration

The deployment script is designed to work seamlessly with GitLab CI/CD. It's automatically invoked by the pipeline defined in `.gitlab-ci.yml`.

### Manual Deployment from GitLab

1. Navigate to **CI/CD** > **Pipelines** in your GitLab project
2. Click on the pipeline for your commit
3. Find the deployment job (`deploy:staging` or `deploy:production:manual`)
4. Click the **Play** button to trigger deployment

### Automatic Deployment

To enable automatic deployments, set the `CONTINUOUS_DEPLOYMENT` variable to `true` in GitLab CI/CD settings:

1. Go to **Settings** > **CI/CD** > **Variables**
2. Add variable `CONTINUOUS_DEPLOYMENT` with value `true`

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `E2B_API_KEY` | E2B API authentication key | `e2b_xxx` |
| `ENVIRONMENT` | Deployment environment | `staging` or `production` |

### Optional Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DEPLOY_URL` | Deployment URL | `https://staging.e2b.dev` |
| `NODE_ENV` | Node.js environment | `production` |
| `DATABASE_URL` | Database connection string | `postgresql://...` |
| `REDIS_URL` | Redis connection string | `redis://...` |

## Security Best Practices

1. **Never commit `.env.staging` or `.env.production` files** - They contain sensitive information
2. **Use GitLab CI/CD variables** for secrets instead of environment files
3. **Enable variable protection** in GitLab for production secrets
4. **Use masked variables** for sensitive values to hide them in logs
5. **Rotate credentials regularly** and update them in GitLab settings

## Troubleshooting

### Issue: Permission denied when running deploy.sh

**Solution:** Make the script executable:
```bash
chmod +x scripts/deployment/deploy.sh
```

### Issue: Missing environment variables

**Solution:** Ensure all required variables are set in your `.env.*` file or GitLab CI/CD variables.

### Issue: Deployment fails with authentication error

**Solution:** 
1. Verify your API keys and tokens are correct
2. Check if tokens have expired
3. Ensure the service account has necessary permissions

## Additional Resources

- [Main GitLab CI/CD Setup Guide](../../GITLAB_CI_SETUP.md)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitLab Environment Variables](https://docs.gitlab.com/ee/ci/variables/)
