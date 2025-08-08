#!/bin/bash

# Startup script for Kids Web Store
echo "🍎 Starting Kids Web Store..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run any migrations or setup if needed
echo "Setting up application..."

# Check if static files exist
if [ ! -f "static/pizza.jpg" ]; then
    echo "⚠️  Warning: Static image files not found in static/ directory"
    echo "   Please copy your food images (pizza.jpg, carrot.jpg, etc.) to the static/ directory"
fi

# Start the application
echo "🚀 Starting application..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000