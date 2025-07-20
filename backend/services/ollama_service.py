import httpx
import json
from typing import Dict, List
import os

class OllamaService:
    def __init__(self):
        """Initialize Ollama client"""
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.default_model = os.getenv("OLLAMA_DEFAULT_MODEL", "gemma:7b")
    
    async def health_check(self) -> bool:
        """Check Ollama connection"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception:
            return False
    
    async def generate_lesson_plan(self, request) -> Dict:
        """Generate a lesson plan using Ollama"""
        prompt = self._build_lesson_plan_prompt(request)
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.default_model,
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
                    lesson_plan = self._parse_lesson_plan_response(
                        result["response"]
                    )
                    
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
                    raise Exception(f"Ollama API error: {response.status_code}")
                    
        except Exception as e:
            raise Exception(f"Failed to generate lesson plan: {str(e)}")
    
    async def generate_worksheet(self, request: Dict) -> Dict:
        """Generate a worksheet using Ollama"""
        prompt = f"""
        Create a worksheet for {request.get('subject')} on the topic {request.get('topic')} 
        for grade {request.get('grade')} students.
        
        Include:
        - 5-10 questions of varying difficulty
        - Clear instructions
        - Answer key
        
        Format as structured content.
        """
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.default_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.6, "num_predict": 1024}
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {"content": result["response"], "type": "worksheet"}
                else:
                    raise Exception(f"Ollama API error: {response.status_code}")
                    
        except Exception as e:
            raise Exception(f"Failed to generate worksheet: {str(e)}")
    
    def _build_lesson_plan_prompt(self, request) -> str:
        """Build the lesson plan generation prompt"""
        grades_str = ", ".join(map(str, request.grades))
        requirements_str = ", ".join(request.requirements)
        
        prompt = f"""
        Create a comprehensive lesson plan for a multi-grade classroom:
        
        Subject: {request.subject}
        Topic: {request.topic}
        Grade Levels: {grades_str}
        Duration: {request.duration} minutes
        Learning Objectives: {request.learning_objectives or "Standard objectives"}
        Special Requirements: {requirements_str}
        
        Structure the lesson plan with:
        1. Learning Objectives (differentiated by grade level)
        2. Materials Needed
        3. Lesson Structure (Introduction, Main Activity, Conclusion)
        4. Activities for each grade level
        5. Assessment methods
        6. Homework/Extension activities
        
        Make it practical for rural Indian classrooms with limited resources.
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
