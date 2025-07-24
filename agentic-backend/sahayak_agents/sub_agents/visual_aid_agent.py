"""Visual Aid Agent for generating educational diagrams and visual prompts."""

from adk import Agent
from typing import Dict, Any, List
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared import (
    VISUAL_AID_AGENT_SYSTEM_PROMPT,
    VISUAL_AID_GENERATION_PROMPT,
    config,
    TaskRequest,
    AgentResponse,
    GradeUtils,
    LanguageUtils,
    get_language_template,
    create_error_response
)


class VisualAidAgent(Agent):
    """Agent specialized in generating simple visual aids for rural classrooms."""
    
    def __init__(self):
        # Use Gemini for rich visual descriptions
        model_name = config.get_model_for_task("visual_aid")
        
        super().__init__(
            model=model_name,
            instructions=VISUAL_AID_AGENT_SYSTEM_PROMPT,
            system_message=VISUAL_AID_AGENT_SYSTEM_PROMPT
        )
    
    def generate_visual_aid(self, request: TaskRequest) -> AgentResponse:
        """Generate a visual aid description based on the request."""
        try:
            # Parse grade levels
            grades = GradeUtils.parse_grade_range(request.grade_level)
            max_grade = max(grades)
            
            # Get language template
            lang_template = get_language_template(request.language)
            
            # Extract learning objective from additional params
            objective = request.additional_params.get(
                "objective", 
                f"Understand {request.topic} concepts"
            )
            
            # Format the generation prompt
            generation_prompt = VISUAL_AID_GENERATION_PROMPT.format(
                topic=request.topic,
                grade_level=request.grade_level,
                subject=request.subject,
                objective=objective,
                language=request.language
            )
            
            # Add specific instructions for rural context and simplicity
            enhanced_prompt = f"""{generation_prompt}

Additional Requirements:
- Use only materials available in rural schools (chalk, blackboard, paper, locally available items)
- Design for teachers with basic artistic skills
- Include familiar objects from rural Indian context
- Make it interactive - students should be able to participate
- Provide alternative materials if chalk/blackboard isn't available
- Consider outdoor learning opportunities using natural materials

Cultural Context:
- Use examples from village life, farming, local festivals
- Include familiar animals, plants, and objects
- Reference local customs and traditions when appropriate
- Use names and scenarios familiar to rural students

Complexity Level:
- Appropriate for grade {max_grade} comprehension
- Simple enough to draw in 5-10 minutes
- Clear enough to see from back of classroom
"""
            
            # Generate visual aid using the agent
            response = self.run(enhanced_prompt)
            
            # Extract visual aid content
            visual_content = response.content if hasattr(response, 'content') else str(response)
            
            # Create metadata
            metadata = {
                "grade_levels": grades,
                "max_grade": max_grade,
                "language": request.language,
                "subject": request.subject,
                "topic": request.topic,
                "objective": objective,
                "materials_needed": self._extract_materials(visual_content),
                "estimated_drawing_time": self._estimate_drawing_time(max_grade),
                "model_used": config.get_model_for_task("visual_aid")
            }
            
            return AgentResponse(
                agent_type="visual_aid_agent",
                content=visual_content,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            return create_error_response(
                "visual_aid_agent",
                f"Error generating visual aid: {str(e)}"
            )
    
    def _extract_materials(self, content: str) -> List[str]:
        """Extract materials needed from the visual aid description."""
        # Basic materials commonly mentioned
        basic_materials = [
            "chalk", "blackboard", "paper", "pencil", "eraser",
            "colored chalk", "ruler", "compass", "stones", "sticks",
            "leaves", "seeds", "rope", "fabric pieces"
        ]
        
        found_materials = []
        content_lower = content.lower()
        
        for material in basic_materials:
            if material in content_lower:
                found_materials.append(material)
        
        # If no specific materials found, provide defaults
        if not found_materials:
            found_materials = ["chalk", "blackboard"]
        
        return found_materials
    
    def _estimate_drawing_time(self, grade_level: int) -> str:
        """Estimate time needed to draw the visual aid."""
        if grade_level <= 3:
            return "5-7 minutes"
        elif grade_level <= 6:
            return "7-10 minutes"
        else:
            return "10-15 minutes"
    
    def validate_visual_aid_request(self, request: TaskRequest) -> tuple[bool, str]:
        """Validate if the request is appropriate for visual aid generation."""
        if not request.topic:
            return False, "Visual aid topic is required"
        
        if not request.subject:
            return False, "Subject area is required for visual aids"
        
        # Check if language is supported
        if not LanguageUtils.validate_language_support(
            request.language,
            config.language.supported_languages
        ):
            return False, f"Language '{request.language}' is not supported"
        
        return True, ""
    
    def suggest_interactive_elements(self, topic: str, grade_level: str) -> Dict[str, List[str]]:
        """Suggest interactive elements to make the visual aid engaging."""
        grades = GradeUtils.parse_grade_range(grade_level)
        max_grade = max(grades)
        
        suggestions = {
            "student_participation": [],
            "hands_on_activities": [],
            "discussion_prompts": [],
            "extension_activities": []
        }
        
        # Age-appropriate participation
        if max_grade <= 3:
            suggestions["student_participation"] = [
                "Students come up to point at different parts",
                "Students add their own drawings",
                "Students make sounds related to the diagram",
                "Students act out parts of the visual"
            ]
        elif max_grade <= 6:
            suggestions["student_participation"] = [
                "Students label parts of the diagram",
                "Students explain connections",
                "Students predict what happens next",
                "Students compare with their own experiences"
            ]
        else:
            suggestions["student_participation"] = [
                "Students analyze and critique the diagram",
                "Students suggest improvements",
                "Students create their own versions",
                "Students present explanations to class"
            ]
        
        # Hands-on activities
        suggestions["hands_on_activities"] = [
            "Build 3D models using local materials",
            "Create their own diagrams",
            "Measure and compare real objects",
            "Collect related items from nature"
        ]
        
        # Discussion prompts
        suggestions["discussion_prompts"] = [
            "What do you notice about...?",
            "How is this similar to things in our village?",
            "What would happen if...?",
            "Can you think of other examples?"
        ]
        
        # Extension activities
        suggestions["extension_activities"] = [
            "Draw the same concept from different angles",
            "Show the concept in different seasons",
            "Connect to other subjects",
            "Share with families at home"
        ]
        
        return suggestions
    
    def generate_alternative_formats(self, visual_content: str, request: TaskRequest) -> Dict[str, str]:
        """Generate alternative formats for different classroom constraints."""
        alternatives = {}
        
        # Paper-based version
        paper_prompt = f"""
        Convert this blackboard visual aid to a paper-based activity:
        
        {visual_content}
        
        Create instructions for:
        1. A worksheet version students can complete
        2. A cut-and-paste activity
        3. A simple handout for take-home reference
        
        Use {request.language} and ensure it works without color printing.
        """
        
        # Outdoor version
        outdoor_prompt = f"""
        Adapt this visual aid for outdoor learning:
        
        {visual_content}
        
        Create instructions for:
        1. Using natural materials (stones, sticks, leaves)
        2. Drawing in sand or dirt
        3. Using the playground or school yard
        4. Group activities in open space
        
        Format in {request.language}.
        """
        
        try:
            # Generate alternatives
            paper_response = self.run(paper_prompt)
            outdoor_response = self.run(outdoor_prompt)
            
            alternatives["paper_based"] = paper_response.content if hasattr(paper_response, 'content') else str(paper_response)
            alternatives["outdoor_learning"] = outdoor_response.content if hasattr(outdoor_response, 'content') else str(outdoor_response)
            
        except Exception as e:
            alternatives["error"] = f"Could not generate alternatives: {str(e)}"
        
        return alternatives
