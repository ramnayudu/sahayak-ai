#!/bin/bash

# Start script for Sahayak AI Streamlit App with ADK Backend
# This script starts both the FastAPI backend and Streamlit frontend

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required dependencies are installed
check_dependencies() {
    log_info "Checking dependencies..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed"
        exit 1
    fi
    
    # Check if we're in the right directory
    if [ ! -f "streamlit_app.py" ]; then
        log_error "streamlit_app.py not found. Please run this script from the project root."
        exit 1
    fi
    
    if [ ! -d "agentic-backend" ]; then
        log_error "agentic-backend directory not found"
        exit 1
    fi
    
    log_success "Dependencies check passed"
}

# Install Python packages
install_packages() {
    log_info "Installing Python packages..."
    
    # Install streamlit requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        log_success "Streamlit dependencies installed"
    fi
    
    # Install backend dependencies with Poetry
    cd agentic-backend
    if command -v poetry &> /dev/null; then
        log_info "Using Poetry to install backend dependencies..."
        poetry install
    else
        log_warning "Poetry not found, trying pip..."
        if [ -f "pyproject.toml" ]; then
            pip install fastapi uvicorn python-dotenv pydantic
            # Note: ADK dependencies may need special installation
            log_warning "Some ADK dependencies may need manual installation"
        fi
    fi
    cd ..
    
    log_success "Package installation completed"
}

# Start the backend server
start_backend() {
    log_info "Starting Sahayak ADK Backend Server..."
    
    cd agentic-backend
    
    # Check if we can import the agent
    python3 -c "from sahayakai.agent import root_agent; print(f'Agent loaded: {root_agent.name}')" 2>/dev/null
    if [ $? -eq 0 ]; then
        log_success "ADK agent loaded successfully"
    else
        log_warning "ADK agent may not be properly configured"
    fi
    
    # Start the server in background
    log_info "Starting FastAPI server on http://localhost:8000"
    python3 server.py &
    BACKEND_PID=$!
    
    cd ..
    
    # Wait for backend to start
    log_info "Waiting for backend to start..."
    sleep 5
    
    # Test backend connection
    if curl -s http://localhost:8000/health > /dev/null; then
        log_success "Backend server is running on http://localhost:8000"
        log_info "API Documentation: http://localhost:8000/docs"
    else
        log_warning "Backend may still be starting up..."
    fi
    
    echo $BACKEND_PID > .backend_pid
}

# Start the Streamlit app
start_streamlit() {
    log_info "Starting Streamlit app..."
    
    # Check if streamlit is installed
    if ! command -v streamlit &> /dev/null; then
        log_error "Streamlit is not installed. Installing..."
        pip install streamlit
    fi
    
    log_info "Starting Streamlit on http://localhost:8501"
    streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0 &
    STREAMLIT_PID=$!
    
    echo $STREAMLIT_PID > .streamlit_pid
    
    # Wait for Streamlit to start
    sleep 3
    log_success "Streamlit app is running on http://localhost:8501"
}

# Cleanup function
cleanup() {
    log_info "Shutting down services..."
    
    if [ -f ".backend_pid" ]; then
        BACKEND_PID=$(cat .backend_pid)
        kill $BACKEND_PID 2>/dev/null || true
        rm .backend_pid
        log_info "Backend server stopped"
    fi
    
    if [ -f ".streamlit_pid" ]; then
        STREAMLIT_PID=$(cat .streamlit_pid)
        kill $STREAMLIT_PID 2>/dev/null || true
        rm .streamlit_pid
        log_info "Streamlit app stopped"
    fi
    
    log_success "Cleanup completed"
    exit 0
}

# Set up signal handlers for cleanup
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    echo "=================================================================="
    echo "🎓 Sahayak AI - Starting Streamlit App with ADK Backend"
    echo "=================================================================="
    echo ""
    
    check_dependencies
    
    # Ask if user wants to install packages
    read -p "Install/update Python packages? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_packages
    fi
    
    echo ""
    log_info "Starting services..."
    
    # Start backend
    start_backend
    
    # Start frontend
    start_streamlit
    
    echo ""
    echo "=================================================================="
    log_success "🎉 Sahayak AI is now running!"
    echo "=================================================================="
    echo ""
    echo "📱 Streamlit App:     http://localhost:8501"
    echo "🔧 Backend API:       http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop all services"
    echo ""
    
    # Keep the script running
    while true; do
        sleep 1
    done
}

# Run main function
main "$@"
