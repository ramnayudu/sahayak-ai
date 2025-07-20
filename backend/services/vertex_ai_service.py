from google.cloud import aiplatform
import vertexai
from vertexai.language_models import TextGenerationModel, ChatModel
from typing import Dict, List
import os
import json

class VertexAIService:
    def __init__(self):
        """Initialize Vertex AI client"""
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        vertexai.init(project=project_id, location=location)
        
        # Initialize models
        self.text_model = TextGenerationModel.from_pretrained("text-bison")
        self.chat_model = ChatModel.from_pretrained("chat-bison")
    
    async def health_check(self) -> bool:
        """Check Vertex AI connection"""
        try:
            # Test with a simple prediction
            response = self.text_model.predict("Hello", max_output_tokens=10)
            return bool(response.text)
        except Exception:
            return False
    
    async def generate_lesson_plan(self, request) -> Dict:
        """Generate a lesson plan using Vertex AI"""
        prompt = self._build_lesson_plan_prompt(request)
        
        try:
            response = self.text_model.predict(
                prompt=prompt,
                max_output_tokens=2048,
                temperature=0.7,
                top_p=0.8
            )
            
            # Parse the response and structure it
            lesson_plan = self._parse_lesson_plan_response(response.text)
            
            return {
                "title": lesson_plan.get("title", f"{request.subject} - {request.topic}"),
                "subject": request.subject,
                "grades": request.grades,
                "topic": request.topic,
                "duration": request.duration,
                "content": lesson_plan,
                "mode": "vertex_ai"
            }
        except Exception as e:
            raise Exception(f"Failed to generate lesson plan: {str(e)}")
    
    async def generate_worksheet(self, request: Dict) -> Dict:
        """Generate a worksheet"""
        prompt = f"""
        Create a worksheet for {request.get('subject')} on the topic {request.get('topic')} 
        for grade {request.get('grade')} students.
        
        Include:
        - 5-10 questions of varying difficulty
        - Clear instructions
        - Answer key
        
        Format as structured JSON.
        """
        
        try:
            response = self.text_model.predict(
                prompt=prompt,
                max_output_tokens=1024,
                temperature=0.6
            )
            
            return {"content": response.text, "type": "worksheet"}
        except Exception as e:
            raise Exception(f"Failed to generate worksheet: {str(e)}")
    
    async def generate_visual_aid(self, request: Dict) -> Dict:
        """Generate visual aid suggestions"""
        prompt = f"""
        Suggest visual aids for teaching {request.get('topic')} in {request.get('subject')} 
        to grade {request.get('grade')} students.
        
        Include:
        - Diagram descriptions
        - Chart suggestions
        - Interactive activity ideas
        - Materials needed
        
        Format as structured suggestions.
        """
        
        try:
            response = self.text_model.predict(
                prompt=prompt,
                max_output_tokens=1024,
                temperature=0.7
            )
            
            return {"content": response.text, "type": "visual_aid"}
        except Exception as e:
            raise Exception(f"Failed to generate visual aid: {str(e)}")
    
    async def generate_assessment(self, request: Dict) -> Dict:
        """Generate student assessment"""
        prompt = f"""
        Create an assessment for {request.get('subject')} on {request.get('topic')} 
        for grade {request.get('grade')} students.
        
        Include:
        - Multiple choice questions (5)
        - Short answer questions (3)
        - One essay question
        - Rubric for grading
        
        Format as structured assessment.
        """
        
        try:
            response = self.text_model.predict(
                prompt=prompt,
                max_output_tokens=1536,
                temperature=0.6
            )
            
            return {"content": response.text, "type": "assessment"}
        except Exception as e:
            raise Exception(f"Failed to generate assessment: {str(e)}")
    
    def _build_lesson_plan_prompt(self, request) -> str:
        """Build the lesson plan generation prompt"""
        grades_str = ", ".join(map(str, request.grades))
        requirements_str = ", ".join(request.requirements)
        
        prompt = f"""
        Create a comprehensive lesson plan for a multi-grade classroom with the following specifications:
        
        Subject: {request.subject}
        Topic: {request.topic}
        Grade Levels: {grades_str}
        Duration: {request.duration} minutes
        Learning Objectives: {request.learning_objectives or "Standard curriculum objectives"}
        Special Requirements: {requirements_str}
        
        Structure the lesson plan with:
        1. Learning Objectives (differentiated by grade level)
        2. Materials Needed
        3. Lesson Structure (Introduction, Main Activity, Conclusion)
        4. Activities for each grade level
        5. Assessment methods
        6. Homework/Extension activities
        7. Adaptations for different learning styles
        
        Make it practical for rural Indian classrooms with limited resources.
        Format as structured JSON.
        """
        
        return prompt
    
    def _parse_lesson_plan_response(self, response_text: str) -> Dict:
        """Parse and structure the lesson plan response"""
        try:
            # Try to parse as JSON first
            return json.loads(response_text)
        except json.JSONDecodeError:
            # If not JSON, structure the text response
            return {
                "content": response_text,
                "format": "text",
                "sections": self._extract_sections(response_text)
            }
    
    def _extract_sections(self, text: str) -> Dict:
        """Extract sections from text response"""
        sections = {}
        current_section = "introduction"
        current_content = []
        
        for line in text.split('\n'):
            line = line.strip()
            if line and line.endswith(':'):
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line[:-1].lower().replace(' ', '_')
                current_content = []
            elif line:
                current_content.append(line)
        
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
