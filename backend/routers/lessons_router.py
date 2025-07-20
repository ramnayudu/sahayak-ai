from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from services.firebase_service import FirebaseService

router = APIRouter()

class LessonPlan(BaseModel):
    id: Optional[str] = None
    title: str
    subject: str
    grades: List[int]
    duration: int
    objectives: List[str]
    content: dict
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@router.get("/", response_model=List[LessonPlan])
async def get_lesson_plans(
    subject: Optional[str] = None,
    grade: Optional[int] = None,
    firebase_service: FirebaseService = Depends()
):
    """Get all lesson plans with optional filtering"""
    try:
        lesson_plans = await firebase_service.get_lesson_plans(
            subject=subject, 
            grade=grade
        )
        return lesson_plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{lesson_id}", response_model=LessonPlan)
async def get_lesson_plan(
    lesson_id: str,
    firebase_service: FirebaseService = Depends()
):
    """Get a specific lesson plan by ID"""
    try:
        lesson_plan = await firebase_service.get_lesson_plan(lesson_id)
        if not lesson_plan:
            raise HTTPException(status_code=404, detail="Lesson plan not found")
        return lesson_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=LessonPlan)
async def create_lesson_plan(
    lesson_plan: LessonPlan,
    firebase_service: FirebaseService = Depends()
):
    """Create a new lesson plan"""
    try:
        created_plan = await firebase_service.create_lesson_plan(
            lesson_plan.dict()
        )
        return created_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{lesson_id}", response_model=LessonPlan)
async def update_lesson_plan(
    lesson_id: str,
    lesson_plan: LessonPlan,
    firebase_service: FirebaseService = Depends()
):
    """Update an existing lesson plan"""
    try:
        updated_plan = await firebase_service.update_lesson_plan(
            lesson_id, 
            lesson_plan.dict()
        )
        return updated_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{lesson_id}")
async def delete_lesson_plan(
    lesson_id: str,
    firebase_service: FirebaseService = Depends()
):
    """Delete a lesson plan"""
    try:
        await firebase_service.delete_lesson_plan(lesson_id)
        return {"message": "Lesson plan deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
