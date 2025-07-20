from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import os
from dotenv import load_dotenv

from routers import ai_router, auth_router, lessons_router
from services.firebase_service import FirebaseService
from services.vertex_ai_service import VertexAIService

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Sahayak AI API",
    description="AI-powered multi-grade classroom assistant API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://sahayak-ai.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize services
firebase_service = FirebaseService()
vertex_ai_service = VertexAIService()

# Include routers
app.include_router(auth_router.router, prefix="/api/auth", tags=["authentication"])
app.include_router(ai_router.router, prefix="/api/ai", tags=["ai"])
app.include_router(lessons_router.router, prefix="/api/lessons", tags=["lessons"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Sahayak AI API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    try:
        # Check Firebase connection
        firebase_status = await firebase_service.health_check()
        
        # Check Vertex AI connection
        vertex_ai_status = await vertex_ai_service.health_check()
        
        return {
            "status": "healthy",
            "services": {
                "firebase": firebase_status,
                "vertex_ai": vertex_ai_status
            }
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@app.get("/api/modes")
async def get_available_modes():
    """Get available AI modes"""
    return {
        "modes": [
            {
                "id": "setu",
                "name": "Sahayak Setu",
                "description": "Online mode with Vertex AI",
                "type": "online",
                "models": ["gemini-pro", "gemma-7b", "gemma-2b"]
            },
            {
                "id": "nivaas", 
                "name": "Sahayak Nivaas",
                "description": "Offline mode with Ollama",
                "type": "offline",
                "models": ["gemma:7b", "gemma:2b"]
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
