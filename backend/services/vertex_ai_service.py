from google.cloud import aiplatform
import vertexai
from vertexai.language_models import TextGenerationModel, ChatModel
from typing import Dict, List
import os
import json
import httpx

class VertexAIService:
    def __init__(self):
        """Initialize Vertex AI client"""
        # Remove dev_mode - always try to use real LLMs
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_DEFAULT_MODEL", "gemma:7b")
        
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        if project_id:
            try:
                vertexai.init(project=project_id, location=location)
                self.text_model = TextGenerationModel.from_pretrained("text-bison")
                self.chat_model = ChatModel.from_pretrained("chat-bison")
            except Exception:
                self.text_model = None
                self.chat_model = None
        else:
            self.text_model = None
            self.chat_model = None
    
    async def health_check(self) -> bool:
        """Check Vertex AI or Ollama connection"""
        # First try Vertex AI
        if self.text_model:
            try:
                response = self.text_model.predict("Hello", max_output_tokens=10)
                if response.text:
                    return True
            except Exception:
                pass
        
        # Fall back to Ollama
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.ollama_base_url}/api/tags", timeout=5.0)
                return response.status_code == 200
        except Exception:
            return False
    
    async def generate_lesson_plan(self, request) -> Dict:
        """Generate a lesson plan using Vertex AI or Ollama as fallback"""
        
        # First try Vertex AI if available
        if self.text_model:
            try:
                prompt = self._build_lesson_plan_prompt(request)
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
                print(f"Vertex AI failed, falling back to Ollama: {e}")
        
        # Fall back to Ollama
        try:
            return await self._generate_with_ollama(request, "lesson_plan")
        except Exception as e:
            raise Exception(f"Both Vertex AI and Ollama failed: {str(e)}")
    
    async def generate_worksheet(self, request: Dict) -> Dict:
        """Generate a worksheet using Vertex AI or Ollama as fallback"""
        
        # First try Vertex AI if available
        if self.text_model:
            try:
                prompt = f"""
                Create a worksheet for {request.get('subject')} on the topic {request.get('topic')} 
                for grade {request.get('grade')} students.
                
                Include:
                - 5-10 questions of varying difficulty
                - Clear instructions
                - Answer key
                
                Format as structured JSON.
                """
                
                response = self.text_model.predict(
                    prompt=prompt,
                    max_output_tokens=1024,
                    temperature=0.6
                )
                
                return {"content": response.text, "type": "worksheet", "mode": "vertex_ai"}
            except Exception as e:
                print(f"Vertex AI failed, falling back to Ollama: {e}")
        
        # Fall back to Ollama
        try:
            return await self._generate_with_ollama(request, "worksheet")
        except Exception as e:
            raise Exception(f"Both Vertex AI and Ollama failed: {str(e)}")
    
    async def generate_visual_aid(self, request: Dict) -> Dict:
        """Generate visual aid suggestions using Vertex AI or Ollama as fallback"""
        
        # First try Vertex AI if available
        if self.text_model:
            try:
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
                
                response = self.text_model.predict(
                    prompt=prompt,
                    max_output_tokens=1024,
                    temperature=0.7
                )
                
                return {"content": response.text, "type": "visual_aid", "mode": "vertex_ai"}
            except Exception as e:
                print(f"Vertex AI failed, falling back to Ollama: {e}")
        
        # Fall back to Ollama
        try:
            return await self._generate_with_ollama(request, "visual_aid")
        except Exception as e:
            raise Exception(f"Both Vertex AI and Ollama failed: {str(e)}")
    
    async def generate_assessment(self, request: Dict) -> Dict:
        """Generate student assessment using Vertex AI or Ollama as fallback"""
        
        # First try Vertex AI if available
        if self.text_model:
            try:
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
                
                response = self.text_model.predict(
                    prompt=prompt,
                    max_output_tokens=1536,
                    temperature=0.6
                )
                
                return {"content": response.text, "type": "assessment", "mode": "vertex_ai"}
            except Exception as e:
                print(f"Vertex AI failed, falling back to Ollama: {e}")
        
        # Fall back to Ollama
        try:
            return await self._generate_with_ollama(request, "assessment")
        except Exception as e:
            raise Exception(f"Both Vertex AI and Ollama failed: {str(e)}")
    
    async def _generate_with_ollama(self, request, content_type: str) -> Dict:
        """Generate content using Ollama as fallback"""
        
        if content_type == "lesson_plan":
            prompt = self._build_lesson_plan_prompt(request)
        elif content_type == "worksheet":
            prompt = f"""
            Create a worksheet for {request.get('subject')} on the topic {request.get('topic')} 
            for grade {request.get('grade')} students.
            
            Include:
            - 5-10 questions of varying difficulty
            - Clear instructions
            - Answer key
            
            Format as structured JSON.
            """
        elif content_type == "visual_aid":
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
        elif content_type == "assessment":
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
        else:
            raise ValueError(f"Unknown content type: {content_type}")
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.8,
                            "num_predict": 2048
                        }
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result.get("response", "")
                    
                    if content_type == "lesson_plan":
                        lesson_plan = self._parse_lesson_plan_response(content)
                        return {
                            "title": f"{request.subject} - {request.topic}",
                            "subject": request.subject,
                            "grades": request.grades,
                            "topic": request.topic,
                            "duration": request.duration,
                            "content": lesson_plan,
                            "mode": "ollama"
                        }
                    else:
                        return {
                            "content": content,
                            "type": content_type,
                            "mode": "ollama"
                        }
                else:
                    raise Exception(f"Ollama API error: {response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to generate {content_type} with Ollama: {str(e)}")

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
