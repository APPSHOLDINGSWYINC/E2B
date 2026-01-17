#!/usr/bin/env bash
set -e

echo "🚀 Starting Render.com build..."

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
pnpm install --frozen-lockfile

# Build Next.js app
echo "🔨 Building Next.js application..."
pnpm build:web

# Run post-build optimizations
echo "⚡ Running optimizations..."
# Clean up any unnecessary files
echo "✅ Build complete!"
