"""
Image Generation Agent for Sahayak AI agent framework.
This agent is responsible for generating visual aids and illustrations.
"""

from typing import Dict, List, Optional, Any
import json
import uuid
from .base_agent import BaseAgent, AgentType, MessageType, AgentMessage
from shared.prompt_templates import VISUAL_AID_TEMPLATE

class ImageGenerationAgent(BaseAgent):
    """
    Agent responsible for generating visual aids and illustrations.
    This agent uses Vertex AI to generate image prompts and descriptions
    for educational content.
    """
    
    def __init__(self, vertex_ai_service):
        """Initialize the image generation agent"""
        super().__init__("image_generator", AgentType.IMAGE_GENERATOR)
        self.vertex_ai_service = vertex_ai_service
    
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process a message received from the orchestrator"""
        if message.message_type == MessageType.REQUEST:
            # Add message to conversation history
            self.conversation_history.append(message)
            
            # Process the request asynchronously
            # In a real implementation, this would be an async call
            # For now, we'll just return a placeholder response
            content = self._generate_image_content(message.content)
            
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
    
    def _generate_image_content(self, request_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate image content based on the request"""
        user_request = request_content.get("user_request", "")
        
        # Extract relevant information from the user request
        subject, topic, grade = self._extract_image_info(user_request)
        
        # Generate image prompts and descriptions
        image_prompts = self._generate_image_prompts(subject, topic, grade)
        
        # In a real implementation, this would call the Vertex AI service
        # to generate image prompts and potentially images
        # For now, we'll just return placeholder responses
        return {
            "visual_aids": [
                {
                    "title": f"{prompt['title']}",
                    "description": f"{prompt['description']}",
                    "image_prompt": f"{prompt['prompt']}",
                    "materials_needed": prompt['materials'],
                    "creation_steps": prompt['steps'],
                    "usage_instructions": prompt['usage']
                }
                for prompt in image_prompts
            ],
            "status": "generated",
            "message": "Visual aids generated successfully"
        }
    
    def _extract_image_info(self, user_request: str) -> tuple:
        """Extract subject, topic, and grade from the user request"""
        # Default values
        subject = "Mathematics"
        topic = "General Concepts"
        grade = 4  # Default to 4th grade
        
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
        
        # Extract grade
        for g in range(1, 13):
            grade_patterns = [f"{g}th grade", f"grade {g}", f"{g}th graders"]
            if any(pattern in user_request.lower() for pattern in grade_patterns):
                grade = g
                break
        
        return subject, topic, grade
    
    def _generate_image_prompts(self, subject: str, topic: str, grade: int) -> List[Dict[str, Any]]:
        """Generate image prompts based on subject, topic, and grade"""
        prompts = []
        
        if subject == "Mathematics" and topic == "Fractions":
            prompts = [
                {
                    "title": "Fraction Circles",
                    "description": "Visual representation of fractions using circular models",
                    "prompt": "Create a colorful illustration of fraction circles showing 1/2, 1/3, 1/4, and 1/6 parts of a whole. Use different colors for each fraction. The illustration should be clear and appropriate for elementary school students.",
                    "materials": ["Colored paper", "Scissors", "Glue", "Markers"],
                    "steps": [
                        "Draw circles of equal size on different colored papers",
                        "Cut one circle into halves, another into thirds, etc.",
                        "Label each piece with its fraction value",
                        "Arrange in a display showing the relationship between fractions"
                    ],
                    "usage": "Use to demonstrate fraction equivalence and comparison"
                },
                {
                    "title": "Fraction Number Line",
                    "description": "Number line showing fractions from 0 to 1",
                    "prompt": "Design a clear, colorful number line from 0 to 1 that shows fractions at their correct positions. Include 1/2, 1/4, 3/4, 1/3, 2/3, etc. Make it visually appealing and easy to understand for 4th grade students.",
                    "materials": ["Chart paper", "Ruler", "Markers", "Colored pencils"],
                    "steps": [
                        "Draw a straight line on chart paper",
                        "Mark 0 at the left end and 1 at the right end",
                        "Divide the line into equal parts based on denominators",
                        "Label each mark with its fraction value",
                        "Use colors to highlight different fraction families"
                    ],
                    "usage": "Use to teach fraction ordering and equivalence"
                },
                {
                    "title": "Fraction Pizza Model",
                    "description": "Pizza-based model for teaching fractions",
                    "prompt": "Illustrate a set of pizzas divided into different fractions (halves, quarters, thirds, etc.). Make the pizzas look appetizing with toppings, and clearly show the division lines. The illustration should be engaging for elementary students.",
                    "materials": ["Cardboard", "Colored paper", "Markers", "Scissors"],
                    "steps": [
                        "Cut circular pieces from cardboard",
                        "Cover with colored paper to represent pizza crust",
                        "Draw division lines to show different fractions",
                        "Add toppings using markers or colored paper",
                        "Label each piece with its fraction value"
                    ],
                    "usage": "Use for hands-on fraction activities and problem-solving"
                }
            ]
        else:
            # Default prompts for other subjects/topics
            prompts = [
                {
                    "title": f"{topic} Visual Aid",
                    "description": f"Visual representation of {topic} concepts",
                    "prompt": f"Create a clear, educational illustration of {topic} concepts appropriate for grade {grade} students. The illustration should be colorful, engaging, and help students understand the key concepts of {topic}.",
                    "materials": ["Chart paper", "Markers", "Colored pencils"],
                    "steps": [
                        "Draw the main concept on chart paper",
                        "Add labels and explanations",
                        "Use colors to highlight important elements",
                        "Add visual examples where appropriate"
                    ],
                    "usage": f"Use to introduce and explain {topic} concepts"
                }
            ]
        
        return prompts
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the image generation agent with the given input data"""
        user_request = input_data.get("user_request", "")
        
        # Extract image information
        subject, topic, grade = self._extract_image_info(user_request)
        
        # Generate image content
        image_content = self._generate_image_content({"user_request": user_request})
        
        return image_content