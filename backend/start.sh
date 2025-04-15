#!/bin/bash

# Configuration
VENV_DIR="backend/venv"
REQUIREMENTS_FILE="backend/requirements.txt"
APP_MODULE="backend.api.app:app"

# Function to check if venv exists
venv_exists() {
    [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/activate" ]
}

# Create virtual environment if it doesn't exist
if ! venv_exists; then
    echo "Creating virtual environment in $VENV_DIR..."
    python -m venv "$VENV_DIR"

    # Check if venv was created successfully
    if ! venv_exists; then
        echo "Failed to create virtual environment"
        exit 1
    fi
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install requirements
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing requirements..."
    pip install --upgrade pip
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "Warning: $REQUIREMENTS_FILE not found. Skipping package installation."
fi

# Run the FastAPI app
echo "Starting Uvicorn server..."
uvicorn "$APP_MODULE" --reload

# Deactivate virtual environment when done
deactivate