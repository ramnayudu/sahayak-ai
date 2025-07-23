"""
Assignment Creation Agent for Sahayak AI agent framework.
This agent is responsible for creating assignments, worksheets, and assessments.
"""

from typing import Dict, List, Optional, Any
import json
import uuid
from .base_agent import BaseAgent, AgentType, MessageType, AgentMessage
from shared.prompt_templates import WORKSHEET_TEMPLATE, ASSESSMENT_TEMPLATE

class AssignmentCreationAgent(BaseAgent):
    """
    Agent responsible for creating assignments, worksheets, and assessments.
    This agent uses Vertex AI to generate educational assignments based on user requests.
    """
    
    def __init__(self, vertex_ai_service):
        """Initialize the assignment creation agent"""
        super().__init__("assignment_creator", AgentType.ASSIGNMENT_CREATOR)
        self.vertex_ai_service = vertex_ai_service
    
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process a message received from the orchestrator"""
        if message.message_type == MessageType.REQUEST:
            # Add message to conversation history
            self.conversation_history.append(message)
            
            # Process the request asynchronously
            # In a real implementation, this would be an async call
            # For now, we'll just return a placeholder response
            content = self._generate_assignment_content(message.content)
            
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
    
    def _generate_assignment_content(self, request_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate assignment content based on the request"""
        user_request = request_content.get("user_request", "")
        
        # Extract relevant information from the user request
        subject, topic, grade = self._extract_assignment_info(user_request)
        
        # Generate worksheet and assessment content
        worksheet = self._generate_worksheet(subject, topic, grade)
        assessment = self._generate_assessment(subject, topic, grade)
        
        # In a real implementation, this would call the Vertex AI service
        # For now, we'll just return placeholder responses
        return {
            "worksheet": worksheet,
            "assessment": assessment,
            "status": "generated",
            "message": "Assignment content generated successfully"
        }
    
    def _extract_assignment_info(self, user_request: str) -> tuple:
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
    
    def _generate_worksheet(self, subject: str, topic: str, grade: int) -> Dict[str, Any]:
        """Generate a worksheet based on subject, topic, and grade"""
        if subject == "Mathematics" and topic == "Fractions":
            # Fractions worksheet for 4th grade
            if grade == 4:
                return {
                    "title": "Understanding Fractions Worksheet",
                    "subject": subject,
                    "topic": topic,
                    "grade": grade,
                    "instructions": "Complete the following problems to practice your understanding of fractions.",
                    "sections": [
                        {
                            "title": "Identifying Fractions",
                            "description": "Write the fraction that represents the shaded part of each shape.",
                            "questions": [
                                "Circle with 1/2 shaded",
                                "Rectangle with 1/4 shaded",
                                "Square with 3/4 shaded"
                            ]
                        },
                        {
                            "title": "Equivalent Fractions",
                            "description": "Fill in the missing numerator or denominator to make equivalent fractions.",
                            "questions": [
                                "1/2 = ?/4",
                                "2/3 = 4/?",
                                "?/5 = 6/10"
                            ]
                        },
                        {
                            "title": "Comparing Fractions",
                            "description": "Compare the fractions using <, >, or =.",
                            "questions": [
                                "1/2 ___ 2/4",
                                "3/4 ___ 2/3",
                                "1/3 ___ 2/6"
                            ]
                        },
                        {
                            "title": "Adding Fractions",
                            "description": "Add the fractions with like denominators.",
                            "questions": [
                                "1/4 + 2/4 = ?",
                                "1/6 + 3/6 = ?",
                                "2/8 + 5/8 = ?"
                            ]
                        },
                        {
                            "title": "Word Problems",
                            "description": "Solve the following word problems involving fractions.",
                            "questions": [
                                "Maya ate 1/4 of a pizza and her brother ate 2/4 of the pizza. How much of the pizza did they eat altogether?",
                                "Raj has 3/4 of a meter of ribbon. He uses 1/4 of a meter to wrap a gift. How much ribbon does he have left?",
                                "A recipe calls for 2/3 cup of flour. If you want to make 1/2 of the recipe, how much flour do you need?"
                            ]
                        }
                    ],
                    "answer_key": {
                        "Identifying Fractions": ["1/2", "1/4", "3/4"],
                        "Equivalent Fractions": ["2", "6", "3"],
                        "Comparing Fractions": ["=", ">", "="],
                        "Adding Fractions": ["3/4", "4/6 or 2/3", "7/8"],
                        "Word Problems": ["3/4", "2/4 or 1/2", "1/3"]
                    }
                }
        
        # Default worksheet for other subjects/topics
        return {
            "title": f"{topic} Worksheet",
            "subject": subject,
            "topic": topic,
            "grade": grade,
            "instructions": f"Complete the following problems to practice your understanding of {topic}.",
            "sections": [
                {
                    "title": f"Understanding {topic}",
                    "description": f"Answer the following questions about {topic}.",
                    "questions": [
                        f"What is {topic}?",
                        f"Give an example of {topic} in real life.",
                        f"Why is {topic} important?"
                    ]
                },
                {
                    "title": f"Practicing {topic}",
                    "description": f"Solve the following problems related to {topic}.",
                    "questions": [
                        "Problem 1",
                        "Problem 2",
                        "Problem 3"
                    ]
                }
            ],
            "answer_key": {
                f"Understanding {topic}": ["Answer 1", "Answer 2", "Answer 3"],
                f"Practicing {topic}": ["Solution 1", "Solution 2", "Solution 3"]
            }
        }
    
    def _generate_assessment(self, subject: str, topic: str, grade: int) -> Dict[str, Any]:
        """Generate an assessment based on subject, topic, and grade"""
        if subject == "Mathematics" and topic == "Fractions":
            # Fractions assessment for 4th grade
            if grade == 4:
                return {
                    "title": "Fractions Assessment",
                    "subject": subject,
                    "topic": topic,
                    "grade": grade,
                    "components": [
                        {
                            "type": "formative",
                            "title": "Quick Check Questions",
                            "items": [
                                "What is a fraction?",
                                "How do you know if two fractions are equivalent?",
                                "When adding fractions, what must be true about the denominators?"
                            ]
                        },
                        {
                            "type": "summative",
                            "title": "End of Unit Assessment",
                            "items": [
                                {
                                    "type": "multiple_choice",
                                    "question": "Which fraction is equivalent to 1/2?",
                                    "options": ["2/4", "1/4", "2/3", "3/4"],
                                    "answer": "2/4"
                                },
                                {
                                    "type": "multiple_choice",
                                    "question": "Which fraction is greater: 2/3 or 3/5?",
                                    "options": ["2/3", "3/5", "They are equal", "Cannot be determined"],
                                    "answer": "2/3"
                                },
                                {
                                    "type": "short_answer",
                                    "question": "What is 1/4 + 2/4?",
                                    "answer": "3/4"
                                },
                                {
                                    "type": "short_answer",
                                    "question": "If you have 3/4 of a pizza and eat 1/4, how much is left?",
                                    "answer": "2/4 or 1/2"
                                },
                                {
                                    "type": "problem_solving",
                                    "question": "A recipe calls for 3/4 cup of sugar. If you want to make 1/2 of the recipe, how much sugar do you need?",
                                    "answer": "3/8 cup"
                                }
                            ]
                        },
                        {
                            "type": "practical",
                            "title": "Hands-On Assessment",
                            "items": [
                                "Using fraction circles, show 3 different ways to represent 1/2.",
                                "Create a fraction number line from 0 to 1, marking 1/4, 1/2, and 3/4.",
                                "Use fraction manipulatives to show that 2/4 = 1/2."
                            ]
                        }
                    ],
                    "rubric": {
                        "criteria": [
                            {
                                "name": "Understanding of Fractions",
                                "levels": [
                                    {"score": 4, "description": "Demonstrates deep understanding of fractions and their relationships"},
                                    {"score": 3, "description": "Shows good understanding of fractions with minor misconceptions"},
                                    {"score": 2, "description": "Basic understanding with some significant misconceptions"},
                                    {"score": 1, "description": "Limited understanding with major misconceptions"}
                                ]
                            },
                            {
                                "name": "Computation Skills",
                                "levels": [
                                    {"score": 4, "description": "Accurately performs all fraction operations"},
                                    {"score": 3, "description": "Performs most fraction operations correctly"},
                                    {"score": 2, "description": "Makes several computational errors"},
                                    {"score": 1, "description": "Unable to perform most fraction operations"}
                                ]
                            },
                            {
                                "name": "Problem Solving",
                                "levels": [
                                    {"score": 4, "description": "Applies fraction concepts to solve complex problems"},
                                    {"score": 3, "description": "Applies fraction concepts to solve straightforward problems"},
                                    {"score": 2, "description": "Applies fraction concepts with guidance"},
                                    {"score": 1, "description": "Unable to apply fraction concepts to solve problems"}
                                ]
                            }
                        ]
                    }
                }
        
        # Default assessment for other subjects/topics
        return {
            "title": f"{topic} Assessment",
            "subject": subject,
            "topic": topic,
            "grade": grade,
            "components": [
                {
                    "type": "formative",
                    "title": "Quick Check Questions",
                    "items": [
                        f"What is {topic}?",
                        f"Why is {topic} important?",
                        f"How do we use {topic} in real life?"
                    ]
                },
                {
                    "type": "summative",
                    "title": "End of Unit Assessment",
                    "items": [
                        {
                            "type": "multiple_choice",
                            "question": f"Question about {topic}",
                            "options": ["Option A", "Option B", "Option C", "Option D"],
                            "answer": "Option A"
                        },
                        {
                            "type": "short_answer",
                            "question": f"Explain {topic} in your own words.",
                            "answer": "Sample answer"
                        }
                    ]
                }
            ],
            "rubric": {
                "criteria": [
                    {
                        "name": f"Understanding of {topic}",
                        "levels": [
                            {"score": 4, "description": "Excellent understanding"},
                            {"score": 3, "description": "Good understanding"},
                            {"score": 2, "description": "Basic understanding"},
                            {"score": 1, "description": "Limited understanding"}
                        ]
                    }
                ]
            }
        }
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the assignment creation agent with the given input data"""
        user_request = input_data.get("user_request", "")
        
        # Extract assignment information
        subject, topic, grade = self._extract_assignment_info(user_request)
        
        # Generate assignment content
        assignment_content = self._generate_assignment_content({"user_request": user_request})
        
        return assignment_content