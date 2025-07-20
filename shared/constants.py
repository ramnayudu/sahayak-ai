# Common constants and utilities for Sahayak AI

# API Response Formats
API_SUCCESS_RESPONSE = {
    "status": "success",
    "data": {},
    "message": "Operation completed successfully"
}

API_ERROR_RESPONSE = {
    "status": "error", 
    "error": {},
    "message": "An error occurred"
}

# Firebase Collections
FIREBASE_COLLECTIONS = {
    "LESSON_PLANS": "lesson_plans",
    "USERS": "users", 
    "USER_PREFERENCES": "user_preferences",
    "WORKSHEETS": "worksheets",
    "ASSESSMENTS": "assessments",
    "VISUAL_AIDS": "visual_aids",
    "STUDENT_PROGRESS": "student_progress",
    "CLASSROOM_DATA": "classroom_data"
}

# AI Model Configurations
VERTEX_AI_MODELS = {
    "GEMINI_PRO": "gemini-pro",
    "GEMMA_7B": "gemma-7b", 
    "GEMMA_2B": "gemma-2b"
}

OLLAMA_MODELS = {
    "GEMMA_7B": "gemma:7b",
    "GEMMA_2B": "gemma:2b",
    "LLAMA2_7B": "llama2:7b"
}

# Indian Education System
NCF_SUBJECTS = {
    "PRIMARY": [
        "Mathematics",
        "Environmental Studies", 
        "Hindi",
        "English",
        "Art Education",
        "Health and Physical Education"
    ],
    "UPPER_PRIMARY": [
        "Mathematics",
        "Science",
        "Social Science",
        "Hindi", 
        "English",
        "Art Education",
        "Health and Physical Education",
        "Work Education"
    ],
    "SECONDARY": [
        "Mathematics",
        "Science",
        "Social Science", 
        "Hindi",
        "English",
        "Third Language",
        "Art Education",
        "Health and Physical Education",
        "Work Education"
    ]
}

# Grade-wise subject mapping
GRADE_SUBJECT_MAPPING = {
    1: ["Mathematics", "Environmental Studies", "Hindi", "English"],
    2: ["Mathematics", "Environmental Studies", "Hindi", "English"], 
    3: ["Mathematics", "Environmental Studies", "Hindi", "English"],
    4: ["Mathematics", "Environmental Studies", "Hindi", "English"],
    5: ["Mathematics", "Environmental Studies", "Hindi", "English"],
    6: ["Mathematics", "Science", "Social Science", "Hindi", "English"],
    7: ["Mathematics", "Science", "Social Science", "Hindi", "English"],
    8: ["Mathematics", "Science", "Social Science", "Hindi", "English"],
    9: ["Mathematics", "Science", "Social Science", "Hindi", "English"],
    10: ["Mathematics", "Science", "Social Science", "Hindi", "English"]
}

# Common lesson durations (in minutes)
LESSON_DURATIONS = [30, 40, 45, 60, 90]

# Assessment types
ASSESSMENT_TYPES = [
    "formative",
    "summative", 
    "peer_assessment",
    "self_assessment",
    "portfolio",
    "performance_based"
]

# Learning objectives categories
LEARNING_OBJECTIVES = {
    "COGNITIVE": [
        "Remember",
        "Understand", 
        "Apply",
        "Analyze",
        "Evaluate",
        "Create"
    ],
    "AFFECTIVE": [
        "Receiving",
        "Responding",
        "Valuing", 
        "Organization",
        "Characterization"
    ],
    "PSYCHOMOTOR": [
        "Perception",
        "Set",
        "Mechanism",
        "Complex Response",
        "Adaptation",
        "Origination"
    ]
}

# Common rural classroom challenges
RURAL_CHALLENGES = [
    "Limited internet connectivity",
    "Insufficient learning materials",
    "Multi-grade teaching",
    "Language barriers",
    "Large class sizes",
    "Irregular attendance",
    "Limited teacher training",
    "Infrastructure constraints"
]

# Available resources in rural schools
TYPICAL_RESOURCES = [
    "Blackboard",
    "Chalk",
    "Basic textbooks", 
    "Chart paper",
    "Colored pencils",
    "Scissors",
    "Glue",
    "Ruler",
    "Local materials (stones, leaves, clay)"
]

# Regional languages (major ones)
REGIONAL_LANGUAGES = [
    "Hindi",
    "Bengali", 
    "Telugu",
    "Marathi",
    "Tamil",
    "Gujarati",
    "Urdu",
    "Kannada",
    "Odia",
    "Malayalam",
    "Punjabi",
    "Assamese"
]

# Content difficulty levels
DIFFICULTY_LEVELS = {
    "BEGINNER": "Basic concepts and recall",
    "INTERMEDIATE": "Application and analysis", 
    "ADVANCED": "Synthesis and evaluation"
}

# Learning modalities
LEARNING_MODALITIES = [
    "visual",
    "auditory",
    "kinesthetic", 
    "reading_writing",
    "multimodal"
]
