#!/bin/bash

echo "================================================"
echo "Google Meet Analytics Backend - Quick Start"
echo "================================================"
echo ""

echo "Step 1/6: Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi
echo "  Python found: $(python3 --version)"

if ! command -v docker &> /dev/null; then
    echo "  Warning: Docker not found. You'll need to install PostgreSQL manually."
else
    echo "  Docker found: $(docker --version)"
fi

echo ""
echo "Step 2/6: Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "  Virtual environment created and activated"

echo ""
echo "Step 3/6: Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "  Dependencies installed"

echo ""
echo "Step 4/6: Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "  .env file created from template"
else
    echo "  .env file already exists"
fi

echo ""
echo "Step 5/6: Starting PostgreSQL..."
if command -v docker &> /dev/null; then
    docker-compose up db -d
    echo "  PostgreSQL started in Docker"
    sleep 5
else
    echo "  Skipping Docker setup. Please ensure PostgreSQL is running."
fi

echo ""
echo "Step 6/6: Initializing database..."
python scripts/init_db.py
echo "  Database initialized"

echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "To start the development server:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Or use:"
echo "  make dev"
echo ""
echo "API will be available at: http://localhost:8000"
echo "API docs: http://localhost:8000/docs"
echo ""
echo "To test model loading (downloads ~4GB on first run):"
echo "  python scripts/test_models.py"
echo ""
echo "================================================"
