# 🛠️ Project Sahayak - Complete Setup Guide

> Step-by-step instructions to set up the AI-Powered Multi-Grade Classroom Assistant

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Node.js 18+** and **npm** ([Download here](https://nodejs.org/))
- **Python 3.9+** ([Download here](https://python.org/))
- **Git** ([Download here](https://git-scm.com/))
- **Google Cloud SDK** (optional, for production deployment)
- **Docker** (optional, for Ollama offline models)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ramnayudu/sahayak-ai.git
cd sahayak-ai
```

### 2. Backend Setup

#### 2.1 Create Python Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

#### 2.2 Install Python Dependencies

```bash
pip install fastapi uvicorn python-multipart
# Additional dependencies as needed:
# pip install firebase-admin google-cloud-aiplatform
```

#### 2.3 Start the Backend Server

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

✅ **Backend should now be running at:** `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs` (Interactive Swagger UI)

### 3. Frontend Setup

#### 3.1 Install Node.js Dependencies

```bash
cd ../frontend  # Navigate to frontend directory
npm install
```

#### 3.2 Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Firebase configuration
nano .env  # or use your preferred editor
```

**Required Environment Variables:**
```bash
# Firebase Configuration
VITE_FIREBASE_API_KEY="your-firebase-api-key"
VITE_FIREBASE_AUTH_DOMAIN="your-project.firebaseapp.com"
VITE_FIREBASE_PROJECT_ID="your-project-id"
VITE_FIREBASE_STORAGE_BUCKET="your-project.firebasestorage.app"
VITE_FIREBASE_MESSAGING_SENDER_ID="your-sender-id"
VITE_FIREBASE_APP_ID="your-app-id"

# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api
VITE_OLLAMA_BASE_URL=http://localhost:11434

# Mode Configuration
VITE_DEFAULT_MODE=online
```

#### 3.3 Start the Frontend Development Server

```bash
npm run dev
```

✅ **Frontend should now be running at:** `http://localhost:3000`

## 🔥 Firebase Setup

### 4.1 Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Create a project"**
3. Enter project name: `ai-sahayak-[your-suffix]`
4. Enable Google Analytics (optional)
5. Create project

### 4.2 Configure Firebase Authentication

1. In Firebase console, go to **Authentication**
2. Click **"Get started"**
3. Go to **Sign-in method** tab
4. Enable **Email/Password** authentication
5. Add authorized domains if needed

### 4.3 Configure Firestore Database

1. Go to **Firestore Database**
2. Click **"Create database"**
3. Choose **"Start in test mode"** for development
4. Select your preferred location
5. Click **"Done"**

### 4.4 Get Firebase Configuration

1. Go to **Project settings** (gear icon)
2. Scroll down to **"Your apps"**
3. Click **"Web app"** icon (`</>`)
4. Register app name: `sahayak-frontend`
5. Copy the configuration object
6. Update your `.env` file with these values

## 🧪 Verify Installation

### 5.1 Test Backend API

Open your browser and visit:
- `http://localhost:8000` - Should show API status
- `http://localhost:8000/api/health` - Should show detailed health check with services status
- `http://localhost:8000/docs` - Should show interactive API documentation (Swagger UI)
- `http://localhost:8000/api/modes` - Should show available AI modes (Setu/Nivaas)

### 5.2 Test Frontend Application

1. Open `http://localhost:3000`
2. You should see the AI Sahayak homepage
3. Navigate through different pages (Dashboard, Lesson Plan, Settings)
4. Check the PWA Status section on the home page

### 5.3 Test Frontend-Backend Communication

1. On the home page, scroll to **"Progressive Web App Status"**
2. The status should show:
   - ✅ Service Worker Active
   - ✅ Secure Context
   - ✅ PWA features working

## 📱 PWA Validation

### 6.1 Built-in PWA Testing

Visit `http://localhost:3000/pwa-validation.html` for comprehensive PWA testing dashboard.

### 6.2 Chrome DevTools Audit

1. Open `http://localhost:3000` in Chrome
2. Press `F12` to open DevTools
3. Go to **Lighthouse** tab
4. Select **Progressive Web App** category
5. Click **"Analyze page load"**
6. Your app should score 80-100 on PWA metrics

### 6.3 Install App Test

1. Look for install icon in browser address bar
2. Click to install the app
3. App should open in standalone mode

## 🔧 Advanced Setup (Optional)

### 7.1 Ollama for Offline AI Models

```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull Gemma models for offline use
ollama pull gemma:2b
ollama pull gemma:7b

# Start Ollama server
ollama serve
```

### 7.2 Google Cloud Vertex AI Setup

```bash
# Install Google Cloud SDK
# Follow: https://cloud.google.com/sdk/docs/install

# Authenticate with Google Cloud
gcloud auth login
gcloud auth application-default login

# Set your project ID
gcloud config set project your-project-id

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
```

## 🚨 Troubleshooting

### Common Issues

**Issue: Frontend shows blank screen**
- Check browser console for errors
- Ensure environment variables are properly set
- Try clearing browser cache and localStorage

**Issue: Backend connection failed**
- Verify backend is running on port 8000
- Check CORS configuration in `main.py`
- Ensure firewall isn't blocking the port
- Visit `/api/health` to check service status

**Issue: API endpoints not working**
- Check if all services are available at `/api/health`
- Verify `.env` configuration is correct
- Check server logs for import errors
- Ensure all required Python packages are installed

**Issue: Firebase authentication not working**
- Verify Firebase configuration in `.env`
- Check if domain is authorized in Firebase console
- Ensure Firebase project has authentication enabled

**Issue: PWA not installable**
- Verify manifest.json is accessible
- Check if HTTPS is enabled (or using localhost)
- Ensure all PWA requirements are met

### Environment-Specific Issues

**macOS:**
- Use `source venv/bin/activate` for virtual environment
- Ensure Xcode command line tools are installed

**Windows:**
- Use `venv\Scripts\activate` for virtual environment
- May need to run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell

**Linux:**
- Ensure Python development headers are installed: `sudo apt-get install python3-dev`
- May need to install additional build tools

## 📁 Project Structure

```
sahayak-ai/
├── backend/
│   ├── venv/              # Python virtual environment
│   ├── main.py            # FastAPI application (main entry point)
│   ├── routers/           # API route handlers
│   │   ├── __init__.py
│   │   ├── auth_router.py     # Authentication endpoints
│   │   ├── ai_router.py       # AI/ML endpoints  
│   │   └── lessons_router.py  # Lesson management endpoints
│   ├── services/          # Business logic services
│   │   ├── __init__.py
│   │   ├── firebase_service.py    # Firebase integration
│   │   ├── vertex_ai_service.py   # Google Cloud AI
│   │   └── ollama_service.py      # Local AI models
│   ├── .env               # Environment configuration
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # App pages
│   │   ├── contexts/      # React contexts (Auth, etc.)
│   │   └── App.jsx        # Main app component
│   ├── public/
│   │   ├── manifest.json  # PWA manifest
│   │   └── *.svg          # PWA icons
│   ├── .env               # Environment variables
│   ├── package.json       # Node.js dependencies
│   └── vite.config.js     # Vite configuration with PWA
├── .gitignore            # Git ignore rules
├── README.md             # Project overview
└── SETUP.md             # This setup guide
```

## 🎯 Next Steps

After successful setup:

1. **Explore the Application**: Navigate through all pages and features
2. **Test PWA Features**: Install the app and test offline functionality
3. **Explore API Documentation**: Visit `http://localhost:8000/docs` for interactive API reference
4. **Test Backend Services**: Check `/api/health` to see service status
5. **Customize Configuration**: Modify Firebase rules, add authentication
6. **Add Content**: Start creating lesson plans and classroom materials
7. **Deploy to Production**: Follow deployment guide for hosting

## 🏗️ Backend Architecture Overview

The backend uses a **modular architecture** designed for scalability:

### **Router Structure**
- **`/api/auth`**: User authentication and session management
- **`/api/ai`**: AI content generation (lesson plans, activities)
- **`/api/lessons`**: Lesson plan CRUD operations and management

### **Service Layer**
- **`FirebaseService`**: Authentication, Firestore database operations
- **`VertexAIService`**: Google Cloud AI integration (Gemini/Gemma models)
- **`OllamaService`**: Local AI models for offline functionality

### **Development Features**
- **Graceful Degradation**: Missing services show as "not_available" instead of crashing
- **Auto-Documentation**: Swagger UI at `/docs` with interactive API testing
- **Hot Reload**: Automatic server restart on code changes
- **Environment Configuration**: `.env` file for easy configuration management

## 🤝 Need Help?

- **Documentation**: Check the README.md for project overview
- **Issues**: Create an issue on GitHub repository
- **Community**: Join our discussions for support and feature requests

---

✅ **Your AI Sahayak setup is now complete!** 🎉

Visit `http://localhost:3000` to start using your AI-powered classroom assistant.
