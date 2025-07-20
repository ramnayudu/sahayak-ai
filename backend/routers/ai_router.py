from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from services.firebase_service import FirebaseService
from services.vertex_ai_service import VertexAIService
from services.ollama_service import OllamaService

router = APIRouter()

class LessonPlanRequest(BaseModel):
    subject: str
    grades: List[int]
    topic: str
    duration: int
    learning_objectives: Optional[str] = None
    requirements: List[str] = []
    mode: str = "online"  # "online" or "offline"

class LessonPlanResponse(BaseModel):
    lesson_plan: dict
    generated_at: str
    mode_used: str

@router.post("/generate-lesson-plan", response_model=LessonPlanResponse)
async def generate_lesson_plan(
    request: LessonPlanRequest,
    firebase_service: FirebaseService = Depends(),
    vertex_ai_service: VertexAIService = Depends(),
    ollama_service: OllamaService = Depends()
):
    """Generate a lesson plan using AI"""
    try:
        if request.mode == "online":
            lesson_plan = await vertex_ai_service.generate_lesson_plan(request)
        else:
            lesson_plan = await ollama_service.generate_lesson_plan(request)
        
        # Save to Firebase
        saved_plan = await firebase_service.save_lesson_plan(lesson_plan)
        
        return LessonPlanResponse(
            lesson_plan=saved_plan,
            generated_at=saved_plan["created_at"],
            mode_used=request.mode
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-worksheet")
async def generate_worksheet(
    request: dict,
    vertex_ai_service: VertexAIService = Depends()
):
    """Generate a worksheet for students"""
    try:
        worksheet = await vertex_ai_service.generate_worksheet(request)
        return {"worksheet": worksheet}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-visual-aid")
async def generate_visual_aid(
    request: dict,
    vertex_ai_service: VertexAIService = Depends()
):
    """Generate visual aids for lessons"""
    try:
        visual_aid = await vertex_ai_service.generate_visual_aid(request)
        return {"visual_aid": visual_aid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assess-student")
async def assess_student(
    request: dict,
    vertex_ai_service: VertexAIService = Depends()
):
    """Generate student assessment"""
    try:
        assessment = await vertex_ai_service.generate_assessment(request)
        return {"assessment": assessment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
