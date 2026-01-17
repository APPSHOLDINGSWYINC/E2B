#!/usr/bin/env bash

# Start Next.js server
if [ "$SERVICE_NAME" = "e2b-web" ] || [ -z "$SERVICE_NAME" ]; then
  echo "Starting Next.js server..."
  pnpm start:web
fi

# Start Python API server
if [ "$SERVICE_NAME" = "e2b-python-api" ]; then
  echo "Starting Python API server..."
  gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120
fi
