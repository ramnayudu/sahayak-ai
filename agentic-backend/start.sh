#!/bin/bash

# Sahayak AI Agentic Backend Startup Script

echo "🚀 Starting Sahayak AI Agentic Backend..."
echo "=" * 50

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the agentic-backend directory"
    exit 1
fi

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Error: Poetry is not installed. Please install Poetry first:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration before running again."
    echo "   Required: GOOGLE_CLOUD_PROJECT, GOOGLE_APPLICATION_CREDENTIALS"
    exit 1
fi

# Install dependencies if needed
echo "📦 Installing dependencies..."
poetry install

# Run system tests
echo "🧪 Running system tests..."
poetry run python test_system.py

if [ $? -ne 0 ]; then
    echo "❌ System tests failed. Please check the configuration."
    exit 1
fi

# Check Google Cloud credentials
echo "🔑 Checking Google Cloud credentials..."
if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "⚠️  Warning: GOOGLE_APPLICATION_CREDENTIALS not set in environment"
    echo "   Make sure to set this environment variable or configure in .env"
fi

if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo "⚠️  Warning: GOOGLE_CLOUD_PROJECT not set in environment"
    echo "   Make sure to set this environment variable or configure in .env"
fi

# Start the API server
echo "🌐 Starting API server on http://localhost:8001..."
echo "📚 API documentation available at: http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Start the server
poetry run python api/main.py
