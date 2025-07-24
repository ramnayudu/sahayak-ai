"""Utility functions for Sahayak agents."""

from typing import Dict, Any, List, Optional, Tuple
import re
import json
from dataclasses import dataclass, field


@dataclass
class TaskRequest:
    """Standardized task request structure."""
    task_type: str  # story, worksheet, visual_aid
    topic: str
    grade_level: str  # e.g., "3", "5-7", "1-3"
    subject: str
    language: str = "en"
    context: str = ""
    additional_params: Dict[str, Any] = field(default_factory=dict)


@dataclass 
class AgentResponse:
    """Standardized agent response structure."""
    agent_type: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error_message: str = ""


class LanguageUtils:
    """Utilities for handling multilingual content."""
    
    @staticmethod
    def detect_language(text: str) -> str:
        """Simple language detection based on script."""
        # Hindi detection (Devanagari script)
        if re.search(r'[\u0900-\u097F]', text):
            return "hi"
        # Telugu detection (Telugu script)
        elif re.search(r'[\u0C00-\u0C7F]', text):
            return "te"
        # Default to English
        else:
            return "en"
    
    @staticmethod
    def validate_language_support(language: str, supported_languages: List[str]) -> bool:
        """Check if language is supported."""
        return language.lower() in [lang.lower() for lang in supported_languages]


class GradeUtils:
    """Utilities for handling grade levels and age groups."""
    
    @staticmethod
    def parse_grade_range(grade_input: str) -> List[int]:
        """Parse grade input like '3', '5-7', '1,3,5' into list of integers."""
        grades = []
        
        # Handle ranges like "5-7"
        if '-' in grade_input:
            start, end = map(int, grade_input.split('-'))
            grades.extend(range(start, end + 1))
        
        # Handle comma-separated like "1,3,5"
        elif ',' in grade_input:
            grades.extend([int(g.strip()) for g in grade_input.split(',')])
        
        # Handle single grade like "3"
        else:
            grades.append(int(grade_input))
        
        return sorted(list(set(grades)))  # Remove duplicates and sort
    
    @staticmethod
    def get_age_group(grades: List[int]) -> str:
        """Get age group description for given grades."""
        min_grade, max_grade = min(grades), max(grades)
        
        if max_grade <= 3:
            return "primary"
        elif min_grade >= 7:
            return "upper_primary"
        elif min_grade <= 3 and max_grade >= 7:
            return "multi_grade"
        else:
            return "middle_primary"
    
    @staticmethod
    def get_difficulty_levels(grades: List[int]) -> Dict[str, List[int]]:
        """Categorize grades into difficulty levels."""
        basic = [g for g in grades if g <= 3]
        intermediate = [g for g in grades if 4 <= g <= 6]
        advanced = [g for g in grades if g >= 7]
        
        return {
            "basic": basic,
            "intermediate": intermediate,
            "advanced": advanced
        }


class ContentUtils:
    """Utilities for content processing and formatting."""
    
    @staticmethod
    def format_for_rural_context(content: str, context_hints: Optional[List[str]] = None) -> str:
        """Add rural Indian context to content."""
        if context_hints is None:
            context_hints = [
                "village", "farm", "rural", "local", "community",
                "festival", "tradition", "family", "nature"
            ]
        
        # This is a simple placeholder - in practice, you might use
        # more sophisticated NLP to inject contextual elements
        return content
    
    @staticmethod
    def estimate_reading_time(text: str, grade_level: int) -> int:
        """Estimate reading time in minutes based on grade level."""
        words = len(text.split())
        
        # Reading speeds by grade (words per minute)
        reading_speeds = {
            1: 30, 2: 50, 3: 70, 4: 90, 5: 110,
            6: 130, 7: 150, 8: 170
        }
        
        wpm = reading_speeds.get(grade_level, 100)
        return max(1, round(words / wpm))
    
    @staticmethod
    def split_by_difficulty(content: str, num_levels: int = 3) -> List[str]:
        """Split content into different difficulty levels."""
        # Simple implementation - split by sentences/paragraphs
        sentences = content.split('.')
        chunk_size = len(sentences) // num_levels
        
        levels = []
        for i in range(num_levels):
            start = i * chunk_size
            end = start + chunk_size if i < num_levels - 1 else len(sentences)
            levels.append('.'.join(sentences[start:end]).strip())
        
        return levels


class ValidationUtils:
    """Utilities for validating inputs and outputs."""
    
    @staticmethod
    def validate_task_request(request: TaskRequest) -> Tuple[bool, str]:
        """Validate a task request."""
        if not request.task_type:
            return False, "Task type is required"
        
        if request.task_type not in ["story", "worksheet", "visual_aid"]:
            return False, f"Invalid task type: {request.task_type}"
        
        if not request.topic:
            return False, "Topic is required"
        
        if not request.grade_level:
            return False, "Grade level is required"
        
        try:
            GradeUtils.parse_grade_range(request.grade_level)
        except ValueError:
            return False, f"Invalid grade level format: {request.grade_level}"
        
        return True, ""
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Basic input sanitization."""
        # Remove potentially harmful characters
        cleaned = re.sub(r'[<>{}[\]\\]', '', text)
        return cleaned.strip()


def create_error_response(agent_type: str, error_message: str) -> AgentResponse:
    """Create a standardized error response."""
    return AgentResponse(
        agent_type=agent_type,
        content="",
        success=False,
        error_message=error_message
    )
