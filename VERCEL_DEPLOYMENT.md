# Vercel Deployment Guide

This guide covers deploying the E2B application to Vercel with zero errors and full functionality.

## 🚀 Quick Start

### Prerequisites

- Node.js >= 18.0.0
- pnpm >= 9.0.0
- Vercel account
- Required API keys (E2B_API_KEY at minimum)

### Installation

```bash
# Install Vercel CLI globally
pnpm install -g vercel

# Login to Vercel
vercel login
```

## 📋 Deployment Steps

### 1. Configure Environment Variables

Set the following environment variables in the Vercel Dashboard:

**Required:**
- `E2B_API_KEY` - Your E2B API key
- `NEXT_PUBLIC_API_URL` - Your app URL (e.g., https://your-app.vercel.app)

**Optional:**
- `ANTHROPIC_API_KEY` - Anthropic API key
- `OPENAI_API_KEY` - OpenAI API key
- `GOOGLE_API_KEY` - Google API key
- `PRODUCTION_URL` - Production URL for asset proxying

### 2. Link Project to Vercel

```bash
cd apps/web
vercel link
```

Follow the prompts to link your project to Vercel.

### 3. Deploy to Production

```bash
# Deploy to production
vercel --prod

# Or use the build and deploy separately
vercel build --prod
vercel deploy --prebuilt --prod
```

## 🔧 Configuration Files

### vercel.json
Located at `apps/web/vercel.json`, this file configures:
- Build settings
- Environment variables
- CORS headers
- Regions and framework settings

### .vercelignore
Located at `apps/web/.vercelignore`, excludes unnecessary files from deployment:
- Dependencies (node_modules)
- Build artifacts
- Test files
- Development tools

## 🧪 Testing Deployment

### Health Check

After deployment, verify the health endpoint:

```bash
curl https://your-app.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-17T12:00:00.000Z",
  "uptime": 123.456,
  "environment": "production",
  "vercel": true,
  "checks": {
    "env": "ok",
    "runtime": "ok"
  }
}
```

### Local Testing

Test the build locally before deploying:

```bash
cd apps/web

# Install dependencies
pnpm install

# Type check
pnpm type-check

# Lint
pnpm lint

# Build
pnpm build

# Start production server
pnpm start
```

## 🔄 CI/CD with GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/vercel-deploy.yml`) that:

1. Runs linting and type checking on every PR
2. Deploys preview builds for PRs
3. Deploys to production on push to main branch

### Required GitHub Secrets

Set these in your GitHub repository settings:

- `VERCEL_TOKEN` - Vercel authentication token
- `VERCEL_ORG_ID` - Your Vercel organization ID
- `VERCEL_PROJECT_ID` - Your Vercel project ID

To get these values:
```bash
# Get your token from https://vercel.com/account/tokens
# Get org and project IDs from .vercel/project.json after linking
cat .vercel/project.json
```

## 🐛 Troubleshooting

### Build Failures

**Error: Module not found**
```bash
# Clean install
rm -rf node_modules .next
pnpm install --frozen-lockfile
pnpm build
```

**Error: Environment variable not defined**
- Ensure all required environment variables are set in Vercel Dashboard
- Check that variable names match exactly (case-sensitive)

**Error: Build exceeded time limit**
- Optimize imports (use modular imports where possible)
- Enable SWC minification in next.config.mjs (already enabled)
- Consider upgrading to Vercel Pro for longer build times

### Runtime Errors

**Error: Function exceeded maximum size**
- Use edge runtime for API routes when possible
- Reduce bundle size by optimizing imports
- Split large functions into smaller ones

**Error: Request timeout**
- Increase function timeout in API route config
- Optimize database queries
- Add caching where appropriate

## 📊 Performance Optimization

### Already Configured

✅ SWC minification enabled  
✅ Image optimization with AVIF/WebP  
✅ Static asset caching (1 year)  
✅ API response caching (60s)  
✅ Vercel Analytics integration  

### Additional Optimizations

1. **Enable ISR (Incremental Static Regeneration)** for frequently updated pages
2. **Use Edge Runtime** for lightweight API routes
3. **Implement CDN caching** for static assets
4. **Monitor bundle size** with webpack analyzer

## 🔐 Security

### Security Headers

Already configured in `next.config.mjs`:
- X-Frame-Options: SAMEORIGIN
- CORS headers for API routes

### Environment Variables

- Never commit `.env` files
- Use Vercel's encrypted environment variables
- Rotate API keys regularly
- Use different keys for production and development

## 📈 Monitoring

### Health Checks

The `/api/health` endpoint provides:
- Application status
- Environment information
- Uptime
- Environment variable validation

### Logs

View logs in Vercel Dashboard:
```
https://vercel.com/[your-username]/[project-name]/deployments
```

## 🆘 Support

If you encounter issues:

1. Check the [Vercel Documentation](https://vercel.com/docs)
2. Review deployment logs in Vercel Dashboard
3. Check GitHub Actions logs for CI/CD issues
4. Verify environment variables are set correctly
5. Test the build locally first

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [E2B Documentation](https://e2b.dev/docs)
