"""Main Orchestrator Agent for Sahayak system."""

from adk import Agent
from typing import Dict, Any, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared import (
    ORCHESTRATOR_SYSTEM_PROMPT,
    config,
    TaskRequest,
    AgentResponse,
    ValidationUtils,
    create_error_response
)
from .sub_agents import StoryAgent, WorksheetAgent, VisualAidAgent


class SahayakOrchestratorAgent(Agent):
    """Main orchestrator agent that routes tasks to specialized sub-agents."""
    
    def __init__(self):
        # Use Gemma for routing decisions (lightweight task)
        model_name = config.get_model_for_task("routing")
        
        super().__init__(
            model=model_name,
            instructions=ORCHESTRATOR_SYSTEM_PROMPT,
            system_message=ORCHESTRATOR_SYSTEM_PROMPT
        )
        
        # Initialize sub-agents
        self.story_agent = StoryAgent()
        self.worksheet_agent = WorksheetAgent()
        self.visual_aid_agent = VisualAidAgent()
        
        # Agent routing map
        self.agent_map = {
            "story": self.story_agent,
            "worksheet": self.worksheet_agent,
            "visual_aid": self.visual_aid_agent
        }
    
    def process_request(self, request: TaskRequest) -> AgentResponse:
        """Process a task request by routing to appropriate sub-agent."""
        try:
            # Validate the request
            is_valid, error_message = ValidationUtils.validate_task_request(request)
            if not is_valid:
                return create_error_response("orchestrator", error_message)
            
            # Route to appropriate agent
            if request.task_type not in self.agent_map:
                return create_error_response(
                    "orchestrator",
                    f"Unknown task type: {request.task_type}"
                )
            
            agent = self.agent_map[request.task_type]
            
            # Generate content using the appropriate agent
            if request.task_type == "story":
                response = agent.generate_story(request)
            elif request.task_type == "worksheet":
                response = agent.generate_worksheet(request)
            elif request.task_type == "visual_aid":
                response = agent.generate_visual_aid(request)
            else:
                return create_error_response(
                    "orchestrator",
                    f"No handler for task type: {request.task_type}"
                )
            
            # Add orchestrator metadata
            if response.success:
                response.metadata["orchestrator_version"] = "0.1.0"
                response.metadata["request_validated"] = True
                response.metadata["routing_successful"] = True
            
            return response
            
        except Exception as e:
            return create_error_response(
                "orchestrator",
                f"Error processing request: {str(e)}"
            )
    
    def analyze_request(self, user_input: str) -> TaskRequest:
        """Analyze user input and create a structured task request."""
        analysis_prompt = f"""
        Analyze this teacher's request and extract the key information:
        
        "{user_input}"
        
        Extract:
        1. Task type (story, worksheet, or visual_aid)
        2. Subject area
        3. Topic
        4. Grade level(s)
        5. Language preference (if mentioned)
        6. Any specific requirements
        
        Respond in JSON format with these fields:
        {{
            "task_type": "...",
            "subject": "...", 
            "topic": "...",
            "grade_level": "...",
            "language": "...",
            "context": "...",
            "confidence": 0.0-1.0
        }}
        """
        
        try:
            response = self.run(analysis_prompt)
            # This would need JSON parsing in a real implementation
            # For now, return a basic request structure
            return self._parse_analysis_response(response, user_input)
            
        except Exception as e:
            # Fallback: create basic request from user input
            return TaskRequest(
                task_type="story",  # Default
                topic=user_input,
                grade_level="3-5",  # Default range
                subject="general",
                language="en",
                context=f"Generated from: {user_input}"
            )
    
    def _parse_analysis_response(self, response, original_input: str) -> TaskRequest:
        """Parse the analysis response into a TaskRequest object."""
        # In a real implementation, this would parse JSON
        # For now, provide intelligent defaults based on keywords
        
        content = response.content if hasattr(response, 'content') else str(response)
        content_lower = content.lower()
        
        # Determine task type from keywords
        task_type = "story"  # default
        if any(word in content_lower for word in ["worksheet", "exercise", "practice", "question"]):
            task_type = "worksheet"
        elif any(word in content_lower for word in ["diagram", "visual", "picture", "draw", "chart"]):
            task_type = "visual_aid"
        elif any(word in content_lower for word in ["story", "tale", "narrative"]):
            task_type = "story"
        
        # Extract subject
        subject = "general"
        subjects = ["math", "science", "english", "hindi", "social", "history", "geography"]
        for subj in subjects:
            if subj in content_lower:
                subject = subj
                break
        
        # Extract grade level
        grade_level = "3-5"  # default
        if "grade" in content_lower:
            # Try to extract specific grades
            import re
            grade_matches = re.findall(r'grade\s*(\d+)', content_lower)
            if grade_matches:
                grade_level = grade_matches[0]
        
        # Extract language
        language = "en"  # default
        if any(lang in content_lower for lang in ["hindi", "हिंदी"]):
            language = "hi"
        elif any(lang in content_lower for lang in ["telugu", "తెలుగు"]):
            language = "te"
        
        return TaskRequest(
            task_type=task_type,
            topic=original_input,
            grade_level=grade_level,
            subject=subject,
            language=language,
            context=f"Analyzed from: {original_input}"
        )
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return information about agent capabilities."""
        return {
            "supported_task_types": ["story", "worksheet", "visual_aid"],
            "supported_languages": config.language.supported_languages,
            "supported_subjects": [
                "Mathematics", "Science", "English", "Hindi", "Telugu",
                "Social Studies", "Environmental Studies", "General Knowledge"
            ],
            "grade_range": "1-8",
            "features": {
                "multilingual_support": True,
                "rural_context_awareness": True,
                "multi_grade_differentiation": True,
                "cultural_sensitivity": True,
                "low_resource_optimization": True
            },
            "sub_agents": {
                "story_agent": {
                    "description": "Generates educational stories",
                    "model": config.get_model_for_task("story")
                },
                "worksheet_agent": {
                    "description": "Creates differentiated worksheets",
                    "model": config.get_model_for_task("worksheet")
                },
                "visual_aid_agent": {
                    "description": "Designs simple visual aids",
                    "model": config.get_model_for_task("visual_aid")
                }
            }
        }
    
    def provide_suggestions(self, incomplete_request: str) -> Dict[str, Any]:
        """Provide suggestions to help teachers complete their requests."""
        suggestions_prompt = f"""
        A teacher has started this request: "{incomplete_request}"
        
        Provide helpful suggestions to complete their request:
        1. What task type would be most helpful?
        2. What additional information is needed?
        3. Suggest appropriate grade levels
        4. Recommend relevant subjects
        5. Suggest ways to make it culturally relevant
        
        Focus on practical suggestions for rural Indian classrooms.
        """
        
        try:
            response = self.run(suggestions_prompt)
            
            # Return structured suggestions
            return {
                "suggested_task_types": ["story", "worksheet", "visual_aid"],
                "missing_information": [
                    "Grade level(s)",
                    "Subject area", 
                    "Specific learning objectives",
                    "Language preference"
                ],
                "cultural_suggestions": [
                    "Include local festivals or traditions",
                    "Use familiar rural examples",
                    "Reference agricultural cycles",
                    "Include community values"
                ],
                "ai_suggestions": response.content if hasattr(response, 'content') else str(response)
            }
            
        except Exception as e:
            return {
                "error": f"Could not generate suggestions: {str(e)}",
                "basic_suggestions": [
                    "Specify the grade level (1-8)",
                    "Mention the subject area",
                    "Describe the learning goal",
                    "Choose preferred language"
                ]
            }
