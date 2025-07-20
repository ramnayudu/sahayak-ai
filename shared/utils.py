# Utility functions for Sahayak AI

import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

def format_api_response(
    data: Any = None, 
    message: str = "Success", 
    status: str = "success"
) -> Dict:
    """Format standardized API response"""
    return {
        "status": status,
        "message": message,
        "data": data,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def format_error_response(
    error: str, 
    details: Optional[Dict] = None
) -> Dict:
    """Format standardized error response"""
    return {
        "status": "error",
        "message": error,
        "details": details or {},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def validate_grade_levels(grades: List[int]) -> bool:
    """Validate if grade levels are valid (1-12)"""
    return all(1 <= grade <= 12 for grade in grades)

def validate_subject(subject: str) -> bool:
    """Validate if subject is in the supported list"""
    from .constants import NCF_SUBJECTS
    
    all_subjects = []
    for grade_subjects in NCF_SUBJECTS.values():
        all_subjects.extend(grade_subjects)
    
    return subject in all_subjects

def extract_grade_appropriate_content(
    content: str, 
    target_grades: List[int]
) -> Dict:
    """Extract grade-appropriate content from generated text"""
    grade_content = {}
    
    for grade in target_grades:
        # Simple heuristic: extract content based on grade mentions
        pattern = rf"grade\s*{grade}[:\-\s]*(.*?)(?=grade\s*\d+|$)"
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if matches:
            grade_content[f"grade_{grade}"] = matches[0].strip()
        else:
            # Fallback: use general content
            grade_content[f"grade_{grade}"] = content
    
    return grade_content

def estimate_reading_level(text: str) -> str:
    """Estimate reading level of given text (simple heuristic)"""
    words = text.split()
    sentences = text.split('.')
    
    if not words or not sentences:
        return "unknown"
    
    avg_word_length = sum(len(word) for word in words) / len(words)
    avg_sentence_length = len(words) / len(sentences)
    
    # Simple heuristic based on average word and sentence length
    if avg_word_length < 4 and avg_sentence_length < 8:
        return "primary"  # Grades 1-5
    elif avg_word_length < 6 and avg_sentence_length < 12:
        return "upper_primary"  # Grades 6-8
    else:
        return "secondary"  # Grades 9-12

def clean_generated_text(text: str) -> str:
    """Clean and format AI-generated text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove markdown-style formatting that might confuse display
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
    
    # Ensure proper sentence spacing
    text = re.sub(r'\.([A-Z])', r'. \1', text)
    
    return text.strip()

def parse_lesson_plan_structure(content: str) -> Dict:
    """Parse lesson plan content into structured sections"""
    sections = {}
    current_section = "introduction"
    current_content = []
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Check if line is a section header
        if re.match(r'^[A-Z\s]+:$|^\d+\.\s*[A-Z]', line):
            # Save previous section
            if current_content:
                sections[current_section] = '\n'.join(current_content)
            
            # Start new section
            current_section = line.lower().replace(':', '').replace('.', '').strip()
            current_section = re.sub(r'[^\w\s]', '', current_section)
            current_section = current_section.replace(' ', '_')
            current_content = []
        else:
            if line:  # Skip empty lines
                current_content.append(line)
    
    # Add the last section
    if current_content:
        sections[current_section] = '\n'.join(current_content)
    
    return sections

def calculate_lesson_complexity(
    grades: List[int], 
    duration: int, 
    requirements: List[str]
) -> str:
    """Calculate lesson complexity based on various factors"""
    complexity_score = 0
    
    # Grade span complexity
    grade_span = max(grades) - min(grades)
    complexity_score += grade_span * 2
    
    # Duration complexity
    if duration > 60:
        complexity_score += 3
    elif duration > 45:
        complexity_score += 2
    else:
        complexity_score += 1
    
    # Requirements complexity
    complexity_score += len(requirements)
    
    # Determine complexity level
    if complexity_score <= 5:
        return "simple"
    elif complexity_score <= 10:
        return "moderate"
    else:
        return "complex"

def generate_activity_id() -> str:
    """Generate unique activity ID"""
    from uuid import uuid4
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid4()).split('-')[0]
    return f"activity_{timestamp}_{unique_id}"

def validate_lesson_plan_data(data: Dict) -> tuple[bool, List[str]]:
    """Validate lesson plan data structure"""
    errors = []
    required_fields = ["subject", "topic", "grades", "duration"]
    
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Validate grades
    if "grades" in data:
        if not isinstance(data["grades"], list):
            errors.append("Grades must be a list")
        elif not validate_grade_levels(data["grades"]):
            errors.append("Invalid grade levels (must be 1-12)")
    
    # Validate duration
    if "duration" in data:
        if not isinstance(data["duration"], int) or data["duration"] <= 0:
            errors.append("Duration must be a positive integer")
    
    # Validate subject
    if "subject" in data and not validate_subject(data["subject"]):
        errors.append(f"Unsupported subject: {data['subject']}")
    
    return len(errors) == 0, errors

def format_indian_date(date_obj: datetime) -> str:
    """Format date in Indian format (DD/MM/YYYY)"""
    return date_obj.strftime("%d/%m/%Y")

def format_indian_currency(amount: float) -> str:
    """Format currency in Indian format (₹)"""
    return f"₹{amount:,.2f}"

def detect_language(text: str) -> str:
    """Simple language detection (English/Hindi)"""
    # Count Devanagari characters
    hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
    total_chars = len(re.sub(r'\s', '', text))
    
    if total_chars == 0:
        return "unknown"
    
    hindi_ratio = hindi_chars / total_chars
    
    if hindi_ratio > 0.3:
        return "hindi"
    else:
        return "english"
