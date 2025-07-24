"""Worksheet Agent for generating differentiated educational exercises."""

from adk import Agent
from typing import Dict, Any, List
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared import (
    WORKSHEET_AGENT_SYSTEM_PROMPT,
    WORKSHEET_GENERATION_PROMPT,
    config,
    TaskRequest,
    AgentResponse,
    GradeUtils,
    LanguageUtils,
    get_language_template,
    create_error_response
)


class WorksheetAgent(Agent):
    """Agent specialized in generating differentiated worksheets for multi-grade classrooms."""
    
    def __init__(self):
        # Use Gemma for structured worksheet content
        model_name = config.get_model_for_task("worksheet")
        
        super().__init__(
            model=model_name,
            instructions=WORKSHEET_AGENT_SYSTEM_PROMPT,
            system_message=WORKSHEET_AGENT_SYSTEM_PROMPT
        )
    
    def generate_worksheet(self, request: TaskRequest) -> AgentResponse:
        """Generate a differentiated worksheet based on the request."""
        try:
            # Parse grade levels
            grades = GradeUtils.parse_grade_range(request.grade_level)
            difficulty_levels = GradeUtils.get_difficulty_levels(grades)
            
            # Get language template
            lang_template = get_language_template(request.language)
            
            # Determine question counts for each level
            question_counts = self._calculate_question_counts(difficulty_levels)
            
            # Extract skills from additional params or default
            skills = request.additional_params.get("skills", "comprehension, application, analysis")
            
            # Format the generation prompt
            generation_prompt = WORKSHEET_GENERATION_PROMPT.format(
                topic=request.topic,
                grade_levels=request.grade_level,
                subject=request.subject,
                language=request.language,
                skills=skills,
                basic_count=question_counts["basic"],
                intermediate_count=question_counts["intermediate"],
                advanced_count=question_counts["advanced"]
            )
            
            # Add specific instructions for rural context
            enhanced_prompt = f"""{generation_prompt}

Additional Requirements:
- Use examples from rural Indian life (farming, local festivals, nature, community)
- Ensure questions can be answered without internet or digital resources
- Include collaborative activities suitable for mixed-age groups
- Provide clear instructions in {request.language}
- Use culturally relevant names and contexts
- Include both individual and group work options

Formatting Instructions:
- Use {lang_template['level']} to label difficulty levels
- Use {lang_template['instructions']} for instruction headers
- Use {lang_template['questions']} for question sections
- Provide answer key with explanations
"""
            
            # Generate worksheet using the agent
            response = self.run(enhanced_prompt)
            
            # Extract worksheet content
            worksheet_content = response.content if hasattr(response, 'content') else str(response)
            
            # Create metadata
            metadata = {
                "grade_levels": grades,
                "difficulty_levels": difficulty_levels,
                "question_counts": question_counts,
                "language": request.language,
                "subject": request.subject,
                "topic": request.topic,
                "skills_targeted": skills,
                "model_used": config.get_model_for_task("worksheet")
            }
            
            return AgentResponse(
                agent_type="worksheet_agent",
                content=worksheet_content,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            return create_error_response(
                "worksheet_agent",
                f"Error generating worksheet: {str(e)}"
            )
    
    def _calculate_question_counts(self, difficulty_levels: Dict[str, List[int]]) -> Dict[str, int]:
        """Calculate appropriate question counts for each difficulty level."""
        counts = {"basic": 0, "intermediate": 0, "advanced": 0}
        
        # Base questions per grade level
        base_questions_per_grade = 2
        
        # Calculate counts based on grades present
        if difficulty_levels["basic"]:
            counts["basic"] = len(difficulty_levels["basic"]) * base_questions_per_grade
        if difficulty_levels["intermediate"]:
            counts["intermediate"] = len(difficulty_levels["intermediate"]) * base_questions_per_grade
        if difficulty_levels["advanced"]:
            counts["advanced"] = len(difficulty_levels["advanced"]) * base_questions_per_grade
        
        # Ensure minimum questions
        for level in counts:
            if counts[level] > 0 and counts[level] < 2:
                counts[level] = 2
        
        return counts
    
    def validate_worksheet_request(self, request: TaskRequest) -> tuple[bool, str]:
        """Validate if the request is appropriate for worksheet generation."""
        if not request.topic:
            return False, "Worksheet topic is required"
        
        if not request.subject:
            return False, "Subject area is required for worksheets"
        
        # Check if language is supported
        if not LanguageUtils.validate_language_support(
            request.language,
            config.language.supported_languages
        ):
            return False, f"Language '{request.language}' is not supported"
        
        return True, ""
    
    def generate_answer_key(self, worksheet_content: str, request: TaskRequest) -> str:
        """Generate a detailed answer key for the worksheet."""
        answer_key_prompt = f"""
        Based on the following worksheet, create a comprehensive answer key:

        {worksheet_content}

        Provide:
        1. Correct answers for all questions
        2. Brief explanations for complex answers
        3. Teaching notes for the instructor
        4. Common mistakes students might make
        5. Extension ideas for advanced students

        Format in {request.language} with clear organization.
        """
        
        try:
            response = self.run(answer_key_prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"Error generating answer key: {str(e)}"
    
    def suggest_adaptations(self, topic: str, grade_range: str) -> Dict[str, List[str]]:
        """Suggest adaptations for different learning needs."""
        grades = GradeUtils.parse_grade_range(grade_range)
        
        adaptations = {
            "visual_learners": [
                "Add simple diagrams or drawings",
                "Use charts and tables for data organization",
                "Include picture-based questions",
                "Provide visual examples"
            ],
            "hands_on_learners": [
                "Include cut-and-paste activities",
                "Add measurement or counting exercises",
                "Incorporate building or construction tasks",
                "Use manipulatives from local materials"
            ],
            "collaborative_learners": [
                "Design pair-work sections",
                "Include group discussion questions",
                "Add peer teaching opportunities",
                "Create team challenge problems"
            ],
            "struggling_learners": [
                "Provide worked examples",
                "Break complex problems into steps",
                "Include vocabulary support",
                "Offer multiple choice options"
            ],
            "advanced_learners": [
                "Add challenge questions",
                "Include open-ended problems",
                "Provide extension activities",
                "Connect to real-world applications"
            ]
        }
        
        return adaptations
