"""
Test script for the agent framework.
This script tests the agent framework with the example scenario:
generating class material and assignment on fractions for 4th graders in Telugu.
"""

import asyncio
import json
from datetime import datetime
from services.vertex_ai_service import VertexAIService
from agents.orchestrator_agent import OrchestratorAgent
from agents.lesson_agent import LessonCreationAgent
from agents.image_agent import ImageGenerationAgent
from agents.assignment_agent import AssignmentCreationAgent
from agents.translation_agent import LanguageTranslationAgent

async def test_agents():
    """Test the agent framework with the example scenario"""
    print("Testing agent framework...")
    
    # Initialize the Vertex AI service
    vertex_ai_service = VertexAIService()
    
    # Initialize the agents
    orchestrator = OrchestratorAgent(vertex_ai_service)
    lesson_agent = LessonCreationAgent(vertex_ai_service)
    image_agent = ImageGenerationAgent(vertex_ai_service)
    assignment_agent = AssignmentCreationAgent(vertex_ai_service)
    translation_agent = LanguageTranslationAgent(vertex_ai_service)
    
    # Register the sub-agents with the orchestrator
    orchestrator.register_agent(lesson_agent)
    orchestrator.register_agent(image_agent)
    orchestrator.register_agent(assignment_agent)
    orchestrator.register_agent(translation_agent)
    
    # Test the example scenario
    user_request = "generate class material and assignment on fractions for 4th graders in telugu"
    
    print(f"User request: {user_request}")
    print("Running orchestrator agent...")
    
    # Run the orchestrator agent
    result = await orchestrator.run({"user_request": user_request})
    
    # Print the result
    print("\nOrchestrator result:")
    print(json.dumps(result, indent=2))
    
    # In a real implementation, we would wait for all sub-agents to complete
    # For now, we'll just run each agent individually
    
    print("\nRunning lesson creation agent...")
    lesson_result = await lesson_agent.run({
        "user_request": user_request,
        "subject": "Mathematics",
        "topic": "Fractions",
        "grades": [4],
        "duration": 45
    })
    
    print("\nLesson creation result:")
    print(json.dumps(lesson_result.get("lesson_plan", {}), indent=2))
    
    print("\nRunning image generation agent...")
    image_result = await image_agent.run({
        "user_request": user_request,
        "subject": "Mathematics",
        "topic": "Fractions",
        "grade": 4
    })
    
    print("\nImage generation result:")
    print(json.dumps(image_result.get("visual_aids", []), indent=2))
    
    print("\nRunning assignment creation agent...")
    assignment_result = await assignment_agent.run({
        "user_request": user_request,
        "subject": "Mathematics",
        "topic": "Fractions",
        "grade": 4
    })
    
    print("\nAssignment creation result:")
    print(json.dumps(assignment_result.get("worksheet", {}), indent=2))
    
    print("\nRunning translation agent...")
    translation_result = await translation_agent.run({
        "user_request": user_request,
        "target_language": "Telugu"
    })
    
    print("\nTranslation result:")
    print(json.dumps(translation_result.get("translated_content", {}), indent=2))
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_agents())