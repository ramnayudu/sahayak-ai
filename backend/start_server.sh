#!/bin/bash

# AI Sahayak Backend Startup Script
# This script ensures the FastAPI server starts correctly with all modules

echo "🚀 Starting AI Sahayak Backend Server..."

# Change to backend directory
cd "$(dirname "$0")"

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment activated: $VIRTUAL_ENV"
else
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

# Install/update dependencies if needed
echo "📋 Checking dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Load environment variables
echo "🔧 Loading environment variables..."
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded"
else
    echo "⚠️  No .env file found, using defaults"
fi

# Start the FastAPI server
echo "🌟 Starting FastAPI server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔄 Auto-reload enabled for development"
echo ""

# Run uvicorn with proper settings
python -m uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --reload-dir . \
    --log-level info \
    --access-log
