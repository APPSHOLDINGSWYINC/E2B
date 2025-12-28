#!/bin/bash
# Deployment script for E2B project
# This script is a TEMPLATE that must be customized for your specific deployment needs
#
# IMPORTANT: This script contains placeholder deployment commands.
# Search for comments like "Add your ... deployment commands here" and replace
# them with your actual deployment commands for your infrastructure.

set -e  # Exit on error
set -u  # Exit on undefined variable

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT="${1:-staging}"
DEPLOYMENT_TYPE="${2:-full}"

echo -e "${GREEN}Starting E2B deployment...${NC}"
echo "Environment: $ENVIRONMENT"
echo "Deployment Type: $DEPLOYMENT_TYPE"
echo "-----------------------------------"

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
    echo -e "${RED}Error: Invalid environment. Use 'staging' or 'production'${NC}"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check required tools
echo "Checking required tools..."
for tool in node pnpm git; do
    if ! command_exists "$tool"; then
        echo -e "${RED}Error: $tool is not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓${NC} $tool is available"
done

# Load environment variables from .env file if it exists
if [ -f ".env.$ENVIRONMENT" ]; then
    echo "Loading environment variables from .env.$ENVIRONMENT"
    # Use safe method to load environment variables
    set -a
    source ".env.$ENVIRONMENT"
    set +a
fi

# Verify required environment variables
echo "Verifying required environment variables..."
REQUIRED_VARS=("E2B_API_KEY")

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var:-}" ]; then
        echo -e "${RED}Error: Required environment variable $var is not set${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓${NC} $var is set"
done

# Install dependencies
echo "Installing dependencies..."
pnpm install --frozen-lockfile

# Build the project
echo "Building the project..."
if [ "$DEPLOYMENT_TYPE" == "full" ]; then
    # Full build including web app
    pnpm run build:web
    pnpm run build --recursive --if-present
elif [ "$DEPLOYMENT_TYPE" == "packages" ]; then
    # Build only packages
    pnpm run build --recursive --if-present
elif [ "$DEPLOYMENT_TYPE" == "web" ]; then
    # Build only web app
    pnpm run build:web
else
    echo -e "${YELLOW}Warning: Unknown deployment type. Performing full build${NC}"
    pnpm run build:web
    pnpm run build --recursive --if-present
fi

# Run deployment based on environment
echo "Deploying to $ENVIRONMENT..."

if [ "$ENVIRONMENT" == "staging" ]; then
    echo "Deploying to staging environment..."
    # Add your staging deployment commands here
    # Examples:
    # - Deploy to staging server: ssh user@staging-server "cd /app && git pull && pnpm install && pnpm run build"
    # - Deploy to cloud platform: gcloud app deploy --project=e2b-staging
    # - Deploy to container registry: docker build -t e2b-staging . && docker push e2b-staging
    echo -e "${YELLOW}Note: Add your staging deployment commands to this script${NC}"
    
elif [ "$ENVIRONMENT" == "production" ]; then
    echo "Deploying to production environment..."

    # Safety check for production (skip if FORCE_DEPLOY=true for CI/CD)
    if [ "${FORCE_DEPLOY:-false}" != "true" ]; then
        if [ -t 0 ]; then
            # Interactive mode
            read -p "Are you sure you want to deploy to PRODUCTION? (yes/no): " confirm
            if [ "$confirm" != "yes" ]; then
                echo -e "${YELLOW}Deployment cancelled${NC}"
                exit 0
            fi
        else
            # Non-interactive mode (CI/CD)
            echo -e "${YELLOW}Warning: Non-interactive mode detected. Set FORCE_DEPLOY=true to bypass confirmation${NC}"
            exit 1
        fi
    else
        echo "FORCE_DEPLOY=true, skipping confirmation"
    fi

    # Add your production deployment commands here
    # Examples:
    # - Deploy to production server: ssh user@prod-server "cd /app && git pull && pnpm install && pnpm run build"
    # - Deploy to cloud platform: gcloud app deploy --project=e2b-production
    # - Deploy to container registry: docker build -t e2b-prod . && docker push e2b-prod
    # - Deploy using deployment tool: vercel deploy --prod
    echo -e "${YELLOW}Note: Add your production deployment commands to this script${NC}"
fi

# Health check (optional)
echo "Running post-deployment health checks..."
# Add health check commands here
# Examples:
# - curl https://$ENVIRONMENT.e2b.dev/health
# - pnpm run test:e2e:$ENVIRONMENT

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo "-----------------------------------"
echo "Environment: $ENVIRONMENT"
echo "Deployment Type: $DEPLOYMENT_TYPE"
echo "Timestamp: $(date)"
echo "-----------------------------------"

# Send notification (optional)
# Examples:
# - Slack: curl -X POST -H 'Content-type: application/json' --data '{"text":"Deployed to '$ENVIRONMENT'"}' $SLACK_WEBHOOK
# - Email: echo "Deployed to $ENVIRONMENT" | mail -s "Deployment Complete" team@example.com
