#!/bin/bash

# Sahayak AI - Complete Setup Script
# This script sets up the entire Sahayak AI monorepo

set -e  # Exit on any error

echo "🎓 Welcome to Sahayak AI Setup"
echo "================================"
echo "Setting up AI-powered multi-grade classroom assistant"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local missing_deps=()
    
    if ! command_exists node; then
        missing_deps+=("Node.js 18+")
    fi
    
    if ! command_exists python3; then
        missing_deps+=("Python 3.9+")
    fi
    
    if ! command_exists git; then
        missing_deps+=("Git")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing prerequisites:"
        for dep in "${missing_deps[@]}"; do
            echo "  - $dep"
        done
        echo ""
        echo "Please install the missing prerequisites and run this script again."
        exit 1
    fi
    
    print_success "All prerequisites found!"
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend (React PWA)..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing frontend dependencies..."
    npm install
    
    # Copy environment file
    if [ ! -f .env ]; then
        cp .env.example .env
        print_warning "Created .env file. Please configure your Firebase settings!"
    fi
    
    print_success "Frontend setup complete!"
    cd ..
}

# Setup backend
setup_backend() {
    print_status "Setting up backend (FastAPI)..."
    
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing backend dependencies..."
    pip install -r requirements.txt
    
    # Copy environment file
    if [ ! -f .env ]; then
        cp .env.example .env
        print_warning "Created .env file. Please configure your Google Cloud and Firebase settings!"
    fi
    
    print_success "Backend setup complete!"
    cd ..
}

# Setup models (Ollama)
setup_models() {
    print_status "Setting up AI models for offline mode..."
    
    cd models
    
    # Make setup script executable
    chmod +x setup.sh
    
    # Ask user if they want to install Ollama and models
    echo ""
    read -p "Do you want to install Ollama and download AI models? This will take several GB of space. (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Installing Ollama and downloading models..."
        ./setup.sh
        print_success "AI models setup complete!"
    else
        print_warning "Skipping AI models setup. You can run ./models/setup.sh later."
    fi
    
    cd ..
}

# Create development scripts
create_dev_scripts() {
    print_status "Creating development scripts..."
    
    # Frontend development script
    cat > start-frontend.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Sahayak AI Frontend..."
cd frontend && npm run dev
EOF
    chmod +x start-frontend.sh
    
    # Backend development script
    cat > start-backend.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Sahayak AI Backend..."
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
EOF
    chmod +x start-backend.sh
    
    # Combined development script
    cat > start-dev.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Sahayak AI Development Environment..."
echo "Frontend will be available at: http://localhost:3000"
echo "Backend will be available at: http://localhost:8000"
echo "API docs will be available at: http://localhost:8000/docs"
echo ""

# Function to kill background processes on exit
cleanup() {
    echo "Shutting down development servers..."
    kill $FRONTEND_PID $BACKEND_PID 2>/dev/null
    exit
}
trap cleanup EXIT

# Start backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "Development servers started!"
echo "Press Ctrl+C to stop all servers"

# Wait for user input
wait
EOF
    chmod +x start-dev.sh
    
    print_success "Development scripts created!"
}

# Display next steps
show_next_steps() {
    echo ""
    echo "🎉 Sahayak AI setup complete!"
    echo "=============================="
    echo ""
    echo "📋 Next Steps:"
    echo ""
    echo "1. Configure environment variables:"
    echo "   - frontend/.env (Firebase configuration)"
    echo "   - backend/.env (Google Cloud and Firebase configuration)"
    echo ""
    echo "2. Start development servers:"
    echo "   ./start-dev.sh           # Start both frontend and backend"
    echo "   ./start-frontend.sh      # Start only frontend"
    echo "   ./start-backend.sh       # Start only backend"
    echo ""
    echo "3. Access the application:"
    echo "   - Frontend: http://localhost:3000"
    echo "   - Backend API: http://localhost:8000"
    echo "   - API Documentation: http://localhost:8000/docs"
    echo ""
    echo "4. For offline mode:"
    echo "   - Run ./models/setup.sh to install Ollama and models"
    echo "   - Ollama will be available at: http://localhost:11434"
    echo ""
    echo "📚 Documentation:"
    echo "   - README.md - Project overview"
    echo "   - docs/deployment.md - Deployment guide"
    echo "   - docs/contributing.md - Contribution guidelines"
    echo ""
    echo "🤝 Need help?"
    echo "   - GitHub Issues: https://github.com/ramnayudu/sahayak-ai/issues"
    echo "   - Email: sahayak.ai@gmail.com"
    echo ""
    echo "Happy coding! 🚀"
}

# Main setup function
main() {
    echo "Starting Sahayak AI setup process..."
    echo ""
    
    check_prerequisites
    echo ""
    
    setup_frontend
    echo ""
    
    setup_backend
    echo ""
    
    setup_models
    echo ""
    
    create_dev_scripts
    echo ""
    
    show_next_steps
}

# Run main function
main
