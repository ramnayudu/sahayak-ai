"""FastAPI backend for Sahayak AI system."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared import TaskRequest, AgentResponse, ValidationUtils
from sahayak_agents import SahayakOrchestratorAgent

# Initialize FastAPI app
app = FastAPI(
    title="Sahayak AI - Educational Agent API",
    description="AI-powered co-teacher for rural multi-grade classrooms in India",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the orchestrator agent
orchestrator = SahayakOrchestratorAgent()

# Pydantic models for API
class GenerateRequest(BaseModel):
    """Request model for content generation."""
    task_type: str  # story, worksheet, visual_aid
    topic: str
    grade_level: str
    subject: str
    language: str = "en"
    context: Optional[str] = None
    additional_params: Optional[Dict[str, Any]] = None

class GenerateResponse(BaseModel):
    """Response model for content generation."""
    success: bool
    content: str
    metadata: Dict[str, Any]
    error_message: Optional[str] = None

class AnalyzeRequest(BaseModel):
    """Request model for analyzing user input."""
    user_input: str
    language: str = "en"

class AnalyzeResponse(BaseModel):
    """Response model for input analysis."""
    success: bool
    task_request: Optional[Dict[str, Any]] = None
    suggestions: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class CapabilitiesResponse(BaseModel):
    """Response model for capabilities."""
    supported_task_types: list
    supported_languages: list
    supported_subjects: list
    grade_range: str
    features: Dict[str, Any]
    sub_agents: Dict[str, Any]

# API Routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Sahayak AI - Educational Agent API",
        "version": "0.1.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test if orchestrator is working
        test_request = TaskRequest(
            task_type="story",
            topic="test",
            grade_level="3",
            subject="general",
            language="en"
        )
        
        # Quick validation test
        is_valid, _ = ValidationUtils.validate_task_request(test_request)
        
        return {
            "status": "healthy",
            "orchestrator_ready": True,
            "validation_working": is_valid,
            "timestamp": "2025-07-23"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2025-07-23"
        }

@app.post("/generate", response_model=GenerateResponse)
async def generate_content(request: GenerateRequest):
    """Generate educational content based on the request."""
    try:
        # Convert to internal task request
        task_request = TaskRequest(
            task_type=request.task_type,
            topic=request.topic,
            grade_level=request.grade_level,
            subject=request.subject,
            language=request.language,
            context=request.context or "",
            additional_params=request.additional_params or {}
        )
        
        # Validate request
        is_valid, error_message = ValidationUtils.validate_task_request(task_request)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)
        
        # Process request through orchestrator
        response = orchestrator.process_request(task_request)
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error_message)
        
        return GenerateResponse(
            success=True,
            content=response.content,
            metadata=response.metadata,
            error_message=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_input(request: AnalyzeRequest):
    """Analyze user input and provide structured task request or suggestions."""
    try:
        # Analyze the user input
        task_request = orchestrator.analyze_request(request.user_input)
        
        # Validate the analyzed request
        is_valid, error_message = ValidationUtils.validate_task_request(task_request)
        
        if is_valid:
            # Return the structured task request
            return AnalyzeResponse(
                success=True,
                task_request={
                    "task_type": task_request.task_type,
                    "topic": task_request.topic,
                    "grade_level": task_request.grade_level,
                    "subject": task_request.subject,
                    "language": task_request.language,
                    "context": task_request.context,
                    "additional_params": task_request.additional_params
                },
                suggestions=None,
                error_message=None
            )
        else:
            # Provide suggestions for improvement
            suggestions = orchestrator.provide_suggestions(request.user_input)
            
            return AnalyzeResponse(
                success=False,
                task_request=None,
                suggestions=suggestions,
                error_message=error_message
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.get("/capabilities", response_model=CapabilitiesResponse)
async def get_capabilities():
    """Get information about agent capabilities."""
    try:
        capabilities = orchestrator.get_capabilities()
        
        return CapabilitiesResponse(
            supported_task_types=capabilities["supported_task_types"],
            supported_languages=capabilities["supported_languages"],
            supported_subjects=capabilities["supported_subjects"],
            grade_range=capabilities["grade_range"],
            features=capabilities["features"],
            sub_agents=capabilities["sub_agents"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting capabilities: {str(e)}")

@app.post("/suggest")
async def get_suggestions(request: AnalyzeRequest):
    """Get suggestions for improving an incomplete request."""
    try:
        suggestions = orchestrator.provide_suggestions(request.user_input)
        
        return {
            "success": True,
            "suggestions": suggestions,
            "input_received": request.user_input
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")

# Additional utility endpoints
@app.get("/tasks/{task_type}/template")
async def get_task_template(task_type: str):
    """Get a template/example for a specific task type."""
    templates = {
        "story": {
            "example_request": {
                "task_type": "story",
                "topic": "friendship",
                "grade_level": "3-5",
                "subject": "moral education",
                "language": "en",
                "context": "rural classroom setting"
            },
            "expected_output": "Educational story with moral lesson, discussion questions, and cultural relevance"
        },
        "worksheet": {
            "example_request": {
                "task_type": "worksheet",
                "topic": "addition and subtraction",
                "grade_level": "2-4",
                "subject": "mathematics",
                "language": "hi",
                "additional_params": {
                    "skills": "basic arithmetic, problem solving"
                }
            },
            "expected_output": "Differentiated worksheet with multiple difficulty levels and answer key"
        },
        "visual_aid": {
            "example_request": {
                "task_type": "visual_aid",
                "topic": "water cycle",
                "grade_level": "4-6",
                "subject": "science",
                "language": "te",
                "additional_params": {
                    "objective": "understand water cycle stages"
                }
            },
            "expected_output": "Simple diagram instructions with step-by-step drawing guide"
        }
    }
    
    if task_type not in templates:
        raise HTTPException(status_code=404, detail=f"Template not found for task type: {task_type}")
    
    return templates[task_type]

@app.get("/languages")
async def get_supported_languages():
    """Get list of supported languages."""
    from shared import config
    
    language_info = {
        "supported_languages": config.language.supported_languages,
        "default_language": config.language.default_language,
        "language_details": {
            "en": {"name": "English", "script": "Latin"},
            "hi": {"name": "Hindi", "script": "Devanagari"},
            "te": {"name": "Telugu", "script": "Telugu"}
        }
    }
    
    return language_info

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,  # Different from existing backend
        reload=True
    )
