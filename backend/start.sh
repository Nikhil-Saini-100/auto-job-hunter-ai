#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "=== Starting Multi-Service Container ==="

# 1. Start local Redis server in background
echo "Starting Redis server..."
redis-server --port 6379 --protected-mode no --daemonize yes

# 2. Wait for Redis to start
sleep 2

# 3. Start Celery worker in the background
echo "Starting Celery worker..."
celery -A app.workers.celery_worker.celery_app worker --loglevel=info --concurrency=1 &

# 4. Run database seeder if requested
if [ "$RUN_SEEDER" = "true" ]; then
    echo "Running database seeder..."
    python -m app.seed
fi

# 5. Start FastAPI application on port 7860 under Uvicorn
echo "Starting FastAPI application on port 7860..."
exec uvicorn app.main:app --host 0.0.0.0 --port 7860
