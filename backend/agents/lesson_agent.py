"""
Lesson Creation Agent for Sahayak AI agent framework.
This agent is responsible for generating educational content and lesson plans.
"""

from typing import Dict, List, Optional, Any
import json
import uuid
from .base_agent import BaseAgent, AgentType, MessageType, AgentMessage
from shared.prompt_templates import LESSON_PLAN_TEMPLATE

class LessonCreationAgent(BaseAgent):
    """
    Agent responsible for generating educational content and lesson plans.
    This agent uses Vertex AI to generate lesson content based on user requests.
    """
    
    def __init__(self, vertex_ai_service):
        """Initialize the lesson creation agent"""
        super().__init__("lesson_creator", AgentType.LESSON_CREATOR)
        self.vertex_ai_service = vertex_ai_service
    
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process a message received from the orchestrator"""
        if message.message_type == MessageType.REQUEST:
            # Add message to conversation history
            self.conversation_history.append(message)
            
            # Process the request asynchronously
            # In a real implementation, this would be an async call
            # For now, we'll just return a placeholder response
            content = self._generate_lesson_content(message.content)
            
            # Create a response message
            response = self.create_message(
                receiver=message.sender,
                message_type=MessageType.RESPONSE,
                content=content,
                conversation_id=message.conversation_id,
                parent_message_id=message.message_id
            )
            
            return response
        
        return None
    
    def _generate_lesson_content(self, request_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate lesson content based on the request"""
        user_request = request_content.get("user_request", "")
        
        # Extract relevant information from the user request
        subject, topic, grades = self._extract_lesson_info(user_request)
        
        # Prepare the lesson plan request
        lesson_request = {
            "subject": subject,
            "topic": topic,
            "grades": grades,
            "duration": 45,  # Default duration
            "student_count": 20,  # Default student count
            "objectives": self._generate_objectives(subject, topic, grades),
            "resources": "Blackboard, textbooks, chart paper, markers"
        }
        
        # In a real implementation, this would call the Vertex AI service
        # For now, we'll just return a placeholder response
        return {
            "lesson_plan": {
                "title": f"Lesson Plan: {topic} for Grade {', '.join(map(str, grades))}",
                "subject": subject,
                "topic": topic,
                "grades": grades,
                "duration": 45,
                "learning_objectives": lesson_request["objectives"],
                "materials_needed": [
                    "Blackboard and chalk",
                    "Chart paper",
                    "Markers",
                    "Textbooks",
                    "Worksheets"
                ],
                "lesson_structure": {
                    "introduction": "Introduction to the topic with real-world examples",
                    "main_activity": "Interactive exploration of the concept",
                    "conclusion": "Summary and assessment of understanding"
                },
                "grade_specific_activities": {
                    f"Grade {grade}": f"Tailored activities for Grade {grade} students" 
                    for grade in grades
                },
                "assessment_methods": [
                    "Formative assessment through questioning",
                    "Worksheet completion",
                    "Group discussion participation"
                ],
                "extension_activities": [
                    "Additional practice problems",
                    "Research project",
                    "Peer teaching opportunity"
                ],
                "teaching_tips": [
                    "Use visual aids to illustrate concepts",
                    "Encourage peer collaboration",
                    "Provide differentiated support as needed"
                ]
            },
            "status": "generated",
            "message": "Lesson plan generated successfully"
        }
    
    def _extract_lesson_info(self, user_request: str) -> tuple:
        """Extract subject, topic, and grades from the user request"""
        # Default values
        subject = "Mathematics"
        topic = "General Concepts"
        grades = [4]  # Default to 4th grade
        
        # Extract subject
        subjects = ["Mathematics", "Science", "English", "Social Studies", "Language Arts"]
        for s in subjects:
            if s.lower() in user_request.lower():
                subject = s
                break
        
        # Extract topic (simple approach - in a real implementation, this would be more sophisticated)
        if "fractions" in user_request.lower():
            topic = "Fractions"
        elif "addition" in user_request.lower():
            topic = "Addition"
        elif "subtraction" in user_request.lower():
            topic = "Subtraction"
        elif "multiplication" in user_request.lower():
            topic = "Multiplication"
        elif "division" in user_request.lower():
            topic = "Division"
        
        # Extract grades
        for grade in range(1, 13):
            grade_patterns = [f"{grade}th grade", f"grade {grade}", f"{grade}th graders"]
            if any(pattern in user_request.lower() for pattern in grade_patterns):
                grades = [grade]
                break
        
        return subject, topic, grades
    
    def _generate_objectives(self, subject: str, topic: str, grades: List[int]) -> str:
        """Generate learning objectives based on subject, topic, and grades"""
        if subject == "Mathematics" and topic == "Fractions":
            if 3 in grades or 4 in grades:
                return "Understand fractions as parts of a whole; Compare fractions; Add and subtract fractions with like denominators"
            elif 5 in grades or 6 in grades:
                return "Add and subtract fractions with unlike denominators; Multiply fractions; Divide fractions"
        
        # Default objectives
        return f"Understand key concepts of {topic} appropriate for grade level; Apply {topic} concepts to solve problems; Communicate understanding of {topic}"
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the lesson creation agent with the given input data"""
        user_request = input_data.get("user_request", "")
        
        # Extract lesson information
        subject, topic, grades = self._extract_lesson_info(user_request)
        
        # Generate lesson content
        lesson_content = self._generate_lesson_content({"user_request": user_request})
        
        return lesson_content