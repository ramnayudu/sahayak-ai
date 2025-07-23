from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from services.firebase_service import FirebaseService
from services.vertex_ai_service import VertexAIService
from services.ollama_service import OllamaService
from agents.orchestrator_agent import OrchestratorAgent
from agents.lesson_agent import LessonCreationAgent
from agents.image_agent import ImageGenerationAgent
from agents.assignment_agent import AssignmentCreationAgent
from agents.translation_agent import LanguageTranslationAgent

router = APIRouter()

# Initialize agent instances at module level
_orchestrator_agent = None
_lesson_agent = None
_image_agent = None
_assignment_agent = None
_translation_agent = None

def get_orchestrator_agent(vertex_ai_service: VertexAIService = Depends()):
    """Get or initialize the orchestrator agent"""
    global _orchestrator_agent
    if _orchestrator_agent is None:
        _orchestrator_agent = OrchestratorAgent(vertex_ai_service)
        
        # Initialize and register sub-agents
        lesson_agent = get_lesson_agent(vertex_ai_service)
        image_agent = get_image_agent(vertex_ai_service)
        assignment_agent = get_assignment_agent(vertex_ai_service)
        translation_agent = get_translation_agent(vertex_ai_service)
        
        _orchestrator_agent.register_agent(lesson_agent)
        _orchestrator_agent.register_agent(image_agent)
        _orchestrator_agent.register_agent(assignment_agent)
        _orchestrator_agent.register_agent(translation_agent)
    
    return _orchestrator_agent

def get_lesson_agent(vertex_ai_service: VertexAIService = Depends()):
    """Get or initialize the lesson creation agent"""
    global _lesson_agent
    if _lesson_agent is None:
        _lesson_agent = LessonCreationAgent(vertex_ai_service)
    return _lesson_agent

def get_image_agent(vertex_ai_service: VertexAIService = Depends()):
    """Get or initialize the image generation agent"""
    global _image_agent
    if _image_agent is None:
        _image_agent = ImageGenerationAgent(vertex_ai_service)
    return _image_agent

def get_assignment_agent(vertex_ai_service: VertexAIService = Depends()):
    """Get or initialize the assignment creation agent"""
    global _assignment_agent
    if _assignment_agent is None:
        _assignment_agent = AssignmentCreationAgent(vertex_ai_service)
    return _assignment_agent

def get_translation_agent(vertex_ai_service: VertexAIService = Depends()):
    """Get or initialize the language translation agent"""
    global _translation_agent
    if _translation_agent is None:
        _translation_agent = LanguageTranslationAgent(vertex_ai_service)
    return _translation_agent

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
    ollama_service: OllamaService = Depends(),
    lesson_agent: LessonCreationAgent = Depends(get_lesson_agent)
):
    """Generate a lesson plan using AI"""
    try:
        if request.mode == "online":
            # Use the lesson creation agent
            agent_input = {
                "user_request": f"Create a lesson plan for {request.subject} on {request.topic} for grade {', '.join(map(str, request.grades))} with duration {request.duration} minutes",
                "subject": request.subject,
                "topic": request.topic,
                "grades": request.grades,
                "duration": request.duration,
                "learning_objectives": request.learning_objectives,
                "requirements": request.requirements
            }
            
            # Run the lesson creation agent
            agent_result = await lesson_agent.run(agent_input)
            lesson_plan = agent_result.get("lesson_plan", {})
        else:
            # Fall back to the original implementation for offline mode
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
    vertex_ai_service: VertexAIService = Depends(),
    assignment_agent: AssignmentCreationAgent = Depends(get_assignment_agent)
):
    """Generate a worksheet for students"""
    try:
        # Extract information from the request
        subject = request.get("subject", "Mathematics")
        topic = request.get("topic", "General Concepts")
        grade = request.get("grade", 4)
        
        # Use the assignment creation agent
        agent_input = {
            "user_request": f"Create a worksheet for {subject} on {topic} for grade {grade} students",
            "subject": subject,
            "topic": topic,
            "grade": grade
        }
        
        # Run the assignment creation agent
        agent_result = await assignment_agent.run(agent_input)
        worksheet = agent_result.get("worksheet", {})
        
        return {"worksheet": worksheet}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-visual-aid")
async def generate_visual_aid(
    request: dict,
    vertex_ai_service: VertexAIService = Depends(),
    image_agent: ImageGenerationAgent = Depends(get_image_agent)
):
    """Generate visual aids for lessons"""
    try:
        # Extract information from the request
        subject = request.get("subject", "Mathematics")
        topic = request.get("topic", "General Concepts")
        grade = request.get("grade", 4)
        
        # Use the image generation agent
        agent_input = {
            "user_request": f"Create visual aids for {subject} on {topic} for grade {grade} students",
            "subject": subject,
            "topic": topic,
            "grade": grade
        }
        
        # Run the image generation agent
        agent_result = await image_agent.run(agent_input)
        visual_aids = agent_result.get("visual_aids", [])
        
        return {"visual_aid": visual_aids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assess-student")
async def assess_student(
    request: dict,
    vertex_ai_service: VertexAIService = Depends(),
    assignment_agent: AssignmentCreationAgent = Depends(get_assignment_agent)
):
    """Generate student assessment"""
    try:
        # Extract information from the request
        subject = request.get("subject", "Mathematics")
        topic = request.get("topic", "General Concepts")
        grade = request.get("grade", 4)
        
        # Use the assignment creation agent
        agent_input = {
            "user_request": f"Create an assessment for {subject} on {topic} for grade {grade} students",
            "subject": subject,
            "topic": topic,
            "grade": grade
        }
        
        # Run the assignment creation agent
        agent_result = await assignment_agent.run(agent_input)
        assessment = agent_result.get("assessment", {})
        
        return {"assessment": assessment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AgentRequest(BaseModel):
    """Request model for the agent-based generation endpoint"""
    user_request: str
    mode: str = "online"  # "online" or "offline"

class AgentResponse(BaseModel):
    """Response model for the agent-based generation endpoint"""
    content: Dict[str, Any]
    conversation_id: str
    status: str
    generated_at: str
    mode_used: str

@router.post("/generate-with-agents", response_model=AgentResponse)
async def generate_with_agents(
    request: AgentRequest,
    firebase_service: FirebaseService = Depends(),
    orchestrator_agent: OrchestratorAgent = Depends(get_orchestrator_agent)
):
    """
    Generate educational content using the agent framework.
    This endpoint uses a main orchestrator agent that coordinates multiple specialized sub-agents.
    """
    try:
        # Run the orchestrator agent with the user request
        result = await orchestrator_agent.run({"user_request": request.user_request})
        
        # In a real implementation, this would wait for all sub-agents to complete
        # For now, we'll just return the initial response
        
        # Save to Firebase (simplified for now)
        timestamp = datetime.now().isoformat()
        saved_content = {
            "content": result,
            "created_at": timestamp,
            "user_request": request.user_request
        }
        
        # In a real implementation, this would save to the appropriate collection
        # await firebase_service.save_content(saved_content)
        
        return AgentResponse(
            content=result,
            conversation_id=result.get("conversation_id", ""),
            status=result.get("status", "processing"),
            generated_at=timestamp,
            mode_used=request.mode
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
