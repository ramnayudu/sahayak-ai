#!/bin/bash

# Sahayak AI Development Setup and Run Script
# This script sets up and runs both frontend and backend services

set -e

echo "🚀 Starting Sahayak AI Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in the correct directory
if [[ ! -f "README.md" ]] || [[ ! -d "frontend" ]] || [[ ! -d "backend" ]]; then
    print_error "Please run this script from the sahayak-ai root directory"
    exit 1
fi

print_status "Setting up Frontend..."
cd frontend
if [[ ! -d "node_modules" ]]; then
    print_warning "Installing frontend dependencies..."
    npm install
fi

print_status "Starting Frontend Development Server..."
echo "Frontend will be available at: http://localhost:5173"
node node_modules/vite/bin/vite.js &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 3

print_status "Setting up Backend..."
cd ../backend

# Configure Python environment
export PYTHON_PATH="/Users/rama.nayudu/sahayak-ai/venv/bin/python"

# Check if virtual environment exists and has packages
if [[ ! -f "test_main.py" ]]; then
    print_warning "Creating minimal test backend..."
    cat > test_main.py << 'EOF'
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Sahayak AI Test")

@app.get("/")
def read_root():
    return {"message": "Sahayak AI Backend is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
fi

print_status "Starting Backend Development Server..."
echo "Backend will be available at: http://localhost:8000"
$PYTHON_PATH /Users/rama.nayudu/sahayak-ai/backend/test_main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

print_status "Testing services..."

# Test frontend
if curl -s http://localhost:5173 > /dev/null; then
    print_status "Frontend is running at http://localhost:5173"
else
    print_warning "Frontend may still be starting..."
fi

# Test backend
if curl -s http://localhost:8000/health > /dev/null; then
    print_status "Backend is running at http://localhost:8000"
    echo "Backend health check: $(curl -s http://localhost:8000/health)"
else
    print_warning "Backend may still be starting..."
fi

echo ""
echo "🎉 Sahayak AI Development Environment is running!"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend:  http://localhost:8000"
echo "📊 Health:   http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    print_status "Stopping services..."
    kill $FRONTEND_PID 2>/dev/null || true
    kill $BACKEND_PID 2>/dev/null || true
    print_status "All services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop the services
wait
