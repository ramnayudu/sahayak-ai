# 🚀 AI Sahayak Backend

FastAPI-based backend for the AI-powered multi-grade classroom assistant with modular architecture.

## 🏗️ Architecture Overview

### Modular Design
```
backend/
├── main.py                 # FastAPI application entry point
├── routers/               # API endpoint organization
│   ├── auth_router.py         # Authentication endpoints
│   ├── ai_router.py           # AI/ML content generation
│   └── lessons_router.py      # Lesson management
├── services/              # Business logic layer
│   ├── firebase_service.py    # Firebase integration
│   ├── vertex_ai_service.py   # Google Cloud AI
│   └── ollama_service.py      # Local AI models
├── .env                   # Environment configuration
└── requirements.txt       # Python dependencies
```

## ✨ Features

- **Modular Architecture** - Organized routers and services
- **FastAPI** - High-performance async web framework with auto-documentation
- **Firebase Integration** - Authentication, Firestore, and Storage
- **Vertex AI Integration** - Google Cloud AI/ML services (Gemini/Gemma)
- **Ollama Support** - Local AI model inference for offline mode
- **Dual AI Modes** - Online (Vertex AI) and Offline (Ollama) operation
- **Development Mode** - Graceful handling of missing external services
- **Interactive Documentation** - Swagger UI at `/docs`

## Tech Stack

- FastAPI
- Firebase Admin SDK
- Google Cloud Vertex AI
- Ollama (for offline mode)
- SQLAlchemy (optional, for additional data)
- Redis (for caching and task queue)
- Celery (for background tasks)

## Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Set up Google Cloud credentials**
   ```bash
   # Download service account key from Google Cloud Console
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
   ```

5. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - User login
- `POST /api/auth/verify-token` - Verify Firebase token
- `GET /api/auth/user-profile` - Get user profile

### AI Services
- `POST /api/ai/generate-lesson-plan` - Generate lesson plan
- `POST /api/ai/generate-worksheet` - Generate worksheet
- `POST /api/ai/generate-visual-aid` - Generate visual aids
- `POST /api/ai/assess-student` - Generate assessments

### Lesson Management
- `GET /api/lessons/` - Get all lesson plans
- `GET /api/lessons/{id}` - Get specific lesson plan
- `POST /api/lessons/` - Create lesson plan
- `PUT /api/lessons/{id}` - Update lesson plan
- `DELETE /api/lessons/{id}` - Delete lesson plan

### System
- `GET /` - Health check
- `GET /api/health` - Detailed health check
- `GET /api/modes` - Get available AI modes

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

1. **Code formatting**
   ```bash
   black .
   isort .
   ```

2. **Linting**
   ```bash
   flake8 .
   ```

3. **Testing**
   ```bash
   pytest
   ```

## Deployment

### Google Cloud Run
```bash
# Build and deploy
gcloud run deploy sahayak-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Docker
```bash
# Build image
docker build -t sahayak-backend .

# Run container
docker run -p 8000:8000 sahayak-backend
```

## Configuration

Key environment variables:
- `GOOGLE_CLOUD_PROJECT` - Google Cloud project ID
- `FIREBASE_SERVICE_ACCOUNT_KEY` - Firebase service account JSON
- `OLLAMA_BASE_URL` - Ollama server URL for offline mode
- `PORT` - Server port (default: 8000)

## Contributing

Please read the main project README for contribution guidelines.
