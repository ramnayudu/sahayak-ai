"""Story Agent for generating educational stories."""

from adk import Agent
from typing import Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared import (
    STORY_AGENT_SYSTEM_PROMPT,
    STORY_GENERATION_PROMPT,
    config,
    TaskRequest,
    AgentResponse,
    GradeUtils,
    LanguageUtils,
    get_language_template,
    create_error_response
)


class StoryAgent(Agent):
    """Agent specialized in generating educational stories for rural classrooms."""
    
    def __init__(self):
        # Use Gemini for rich story content
        model_name = config.get_model_for_task("story")
        
        super().__init__(
            model=model_name,
            instructions=STORY_AGENT_SYSTEM_PROMPT,
            system_message=STORY_AGENT_SYSTEM_PROMPT
        )
    
    def generate_story(self, request: TaskRequest) -> AgentResponse:
        """Generate an educational story based on the request."""
        try:
            # Parse grade level
            grades = GradeUtils.parse_grade_range(request.grade_level)
            age_group = GradeUtils.get_age_group(grades)
            
            # Get language template
            lang_template = get_language_template(request.language)
            
            # Determine story length based on grade level
            max_grade = max(grades)
            if max_grade <= 3:
                word_count = "200-400 words"
            elif max_grade <= 6:
                word_count = "400-600 words"
            else:
                word_count = "600-800 words"
            
            # Format the generation prompt
            generation_prompt = STORY_GENERATION_PROMPT.format(
                topic=request.topic,
                grade_level=request.grade_level,
                language=request.language,
                subject=request.subject,
                context=request.context or "rural Indian classroom setting"
            )
            
            # Add specific instructions for word count and cultural context
            enhanced_prompt = f"""{generation_prompt}

Additional Requirements:
- Story length: {word_count}
- Include cultural elements familiar to rural Indian students
- Use simple, age-appropriate language for grades {request.grade_level}
- Include interactive elements or questions within the story
- End with a clear moral or educational takeaway

Language Instructions:
- Write primarily in {request.language}
- Use {lang_template['greeting']} style greetings if appropriate
- Ensure cultural sensitivity and local relevance
"""
            
            # Generate story using the agent
            response = self.run(enhanced_prompt)
            
            # Extract story content from response
            story_content = response.content if hasattr(response, 'content') else str(response)
            
            # Create metadata
            metadata = {
                "grade_levels": grades,
                "age_group": age_group,
                "target_word_count": word_count,
                "language": request.language,
                "subject": request.subject,
                "topic": request.topic,
                "model_used": config.get_model_for_task("story")
            }
            
            return AgentResponse(
                agent_type="story_agent",
                content=story_content,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            return create_error_response(
                "story_agent", 
                f"Error generating story: {str(e)}"
            )
    
    def validate_story_request(self, request: TaskRequest) -> tuple[bool, str]:
        """Validate if the request is appropriate for story generation."""
        if not request.topic:
            return False, "Story topic is required"
        
        if not request.subject:
            return False, "Subject area is required for educational stories"
        
        # Check if language is supported
        if not LanguageUtils.validate_language_support(
            request.language, 
            config.language.supported_languages
        ):
            return False, f"Language '{request.language}' is not supported"
        
        return True, ""
    
    def suggest_story_enhancements(self, topic: str, grade_level: str) -> Dict[str, Any]:
        """Suggest ways to enhance the story for better engagement."""
        grades = GradeUtils.parse_grade_range(grade_level)
        max_grade = max(grades)
        
        suggestions = {
            "interactive_elements": [],
            "cultural_connections": [],
            "extension_activities": []
        }
        
        # Age-appropriate interactive elements
        if max_grade <= 3:
            suggestions["interactive_elements"] = [
                "Simple sound effects students can make",
                "Basic hand gestures or movements",
                "Repetitive phrases students can join in"
            ]
        elif max_grade <= 6:
            suggestions["interactive_elements"] = [
                "Character voice changes",
                "Prediction questions at key moments", 
                "Simple role-playing opportunities"
            ]
        else:
            suggestions["interactive_elements"] = [
                "Discussion questions about character motivations",
                "Alternative ending brainstorming",
                "Connect to real-world examples"
            ]
        
        # Cultural connections for rural context
        suggestions["cultural_connections"] = [
            "Local festivals and celebrations",
            "Traditional games and activities", 
            "Agricultural cycles and seasons",
            "Family and community structures",
            "Local wildlife and nature"
        ]
        
        # Extension activities
        suggestions["extension_activities"] = [
            "Draw a favorite scene from the story",
            "Act out the story in small groups",
            "Create their own ending",
            "Share similar stories from their families",
            "Connect the story to their own experiences"
        ]
        
        return suggestions
