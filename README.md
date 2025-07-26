# 🎓 Project Sahayak - AI-Powered Multi-Grade Classroom Assistant

> Empowering rural Indian teachers with AI-driven solutions for multi-grade classroom management
#sample commit Surya
## 🎯 Problem Statement

Rural Indian schools often face the challenge of multi-grade classrooms where a single teacher manages students from different grade levels simultaneously. This creates significant difficulties in:
- Personalized lesson planning across multiple grades
- Student assessment and progress tracking
- Resource allocation and time management
- Engaging students with diverse learning levels

**Project Sahayak** addresses these challenges by providing an AI-powered assistant that helps teachers efficiently manage multi-grade classrooms through intelligent content generation, adaptive learning recommendations, and streamlined administrative tasks.

## 🚀 Technology Stack

### Frontend (PWA)
- **React** with **Vite** for fast development
- **Firebase Hosting** for deployment
- **IndexedDB** for offline caching
- Progressive Web App capabilities for mobile access

### Backend
- **Python FastAPI** for high-performance API
- **Google ADK agents** (or LangGraph) for AI orchestration
- **Vertex AI** integration for Gemini/Gemma models
- **Firebase** ecosystem (Firestore, Storage, Auth)

### AI Models
- **Sahayak Setu (Online)**: Gemini + Gemma via Vertex AI
- **Sahayak Nivaas (Offline)**: Quantized Gemma 2B/7B via Ollama
- **SQLite** for local data storage in offline mode

## 📁 Project Structure

```
sahayak-ai/
├── frontend/          # React PWA application
├── backend/           # FastAPI + AI agents
├── models/            # Ollama setup & quantized models
├── shared/            # Common utilities & templates
└── docs/              # Documentation & guides
```

## 🛠️ Getting Started

**Ready to set up Project Sahayak?**

👉 **[Complete Setup Guide](./SETUP.md)** - Follow our step-by-step instructions to get the AI classroom assistant running on your system.

### Quick Links
- 🚀 [Setup Instructions](./SETUP.md) - Complete installation guide
- 📱 [PWA Validation](http://localhost:3000/pwa-validation.html) - Test Progressive Web App features
- 🔧 [API Documentation](http://localhost:8000/docs) - Backend API reference
- 📚 [User Guide](./docs/user-guide.md) - How to use the application

### Technology Requirements
- Node.js 18+ and npm
- Python 3.9+
- Firebase account (free tier available)
- Modern web browser with PWA support

## 🎯 Key Features

- **Dual Mode Operation**: Online (Vertex AI) and Offline (Ollama)
- **Multi-Grade Lesson Planning**: AI-generated content for different grade levels
- **Student Progress Tracking**: Intelligent assessment and recommendations
- **Resource Management**: Optimized allocation of teaching materials
- **Offline-First Design**: Works without internet connectivity
- **Mobile-Optimized**: PWA for smartphone and tablet access

## 🏆 Team & Attribution

**Team AI Wranglers** - BIEC Sprint  
*Google Cloud Agentic AI Day 2025*

### Contributors
- Built with ❤️ for rural education in India
- Powered by Google Cloud Vertex AI and Gemini/Gemma models
- Special thanks to the open-source community and Ollama project

## ⚡ Quick Reference

### Development Servers
- **Frontend**: `http://localhost:3000` (React + Vite)
- **Backend**: `http://localhost:8000` (FastAPI)
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **PWA Test**: `http://localhost:3000/pwa-validation.html`

### Key Commands
```bash
# Start backend
cd backend && source venv/bin/activate && python -m uvicorn main:app --reload

# Start frontend  
cd frontend && npm run dev

# Install as PWA
# Look for install icon in browser address bar
```

### Backend Architecture
- **Modular Design**: Organized with routers and services
- **API Routes**: `/api/auth`, `/api/ai`, `/api/lessons`
- **Service Layer**: Firebase, Vertex AI, and Ollama integration
- **Development Mode**: Graceful handling of missing external services
- **Auto-Documentation**: Interactive API docs at `/docs`

## 📚 Documentation

- 📖 **[Complete Setup Guide](./SETUP.md)** - Detailed installation instructions
- 🏗️ [Frontend Architecture](./frontend/README.md) - React PWA details
- ⚡ [Backend API Guide](./backend/README.md) - FastAPI documentation
- 🤖 [AI Models Guide](./docs/models.md) - Gemini/Gemma integration
- 🚀 [Deployment Guide](./docs/deployment.md) - Production hosting
- 👥 [Contributing Guide](./docs/contributing.md) - Development workflow

## 🎯 Current Features

✅ **Implemented:**
- Progressive Web App (PWA) with offline support
- Firebase Authentication integration
- React-based responsive UI with routing
- **Modular FastAPI backend** with organized routers and services
- **Interactive API documentation** at `/docs`
- **Multi-service architecture** (Firebase, Vertex AI, Ollama ready)
- **Agent-based AI framework** using ADK and A2A protocol
- **Specialized AI agents** for lesson creation, image generation, assignment creation, and language translation
- Real-time PWA status monitoring
- Environment-based configuration
- Modern development setup with Vite

🚧 **In Development:**
- Multi-grade content adaptation
- Student progress tracking
- Offline AI model integration (Ollama)
- Advanced classroom management tools

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](./docs/contributing.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Making quality education accessible to every rural classroom in India* 🇮🇳 

Stream URL 

https://us-central1-aiplatform.googleapis.com/v1/projects/concrete-bridge-466718-s2/locations/us-central1/reasoningEngines/6857390139648245760:streamQuery?alt=sse
