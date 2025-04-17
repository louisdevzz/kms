#!/bin/bash

# Configuration
VENV_DIR="backend/venv"
REQUIREMENTS_FILE="backend/requirements.txt"
APP_MODULE="backend.api.app:app"

# Function to handle cleanup
cleanup() {
    echo "Stopping containers..."
    docker compose -f docker-compose.mongo.yml down
    docker compose -f docker-compose.minio.yml down
    deactivate 2>/dev/null  # Silently deactivate venv if active
    echo "Cleanup complete"
    exit 0
}

trap cleanup SIGINT EXIT

# Start MongoDB container
echo "Starting MongoDB container..."
docker compose -f backend/docker/docker-compose.mongo.yml up -d

# Start MinIO container
echo "Starting MinIO container..."
docker compose -f backend/docker/docker-compose.minio.yml up -d

# Wait for services to initialize
echo "Waiting 2 seconds for services..."
sleep 2

# Virtual environment setup
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install requirements
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing requirements..."
    pip install --upgrade pip
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "Warning: Requirements file not found"
fi

# Run FastAPI app
echo "Starting Uvicorn server..."
uvicorn "$APP_MODULE" --host 0.0.0.0 --port 8000 --reload

