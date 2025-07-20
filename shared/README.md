# Sahayak Shared

Common utilities, templates, and constants shared between frontend and backend.

## Contents

### `prompt_templates.py`
- AI prompt templates for different content types
- Lesson plan generation prompts
- Worksheet creation templates
- Assessment generation templates
- Story creation templates
- Visual aid suggestions

### `constants.py`
- API response formats
- Firebase collection names
- AI model configurations
- Indian education system mappings
- Grade-subject relationships
- Common resources and challenges

### `utils.py`
- API response formatting utilities
- Data validation functions
- Text processing and cleaning
- Lesson plan parsing
- Complexity calculation
- Indian localization helpers

## Usage

### In Backend (Python)
```python
from shared.prompt_templates import LESSON_PLAN_TEMPLATE
from shared.constants import FIREBASE_COLLECTIONS
from shared.utils import format_api_response, validate_grade_levels

# Use prompt template
prompt = LESSON_PLAN_TEMPLATE.format(
    subject="Mathematics",
    topic="Fractions", 
    grades="3, 4",
    duration=45,
    objectives="Understanding basic fractions"
)

# Format API response
response = format_api_response(
    data=lesson_plan,
    message="Lesson plan generated successfully"
)
```

### In Frontend (JavaScript)
```javascript
// Import constants (if using module system)
import { INDIAN_SUBJECTS, GRADE_LEVELS } from './shared/constants'

// Use in components
const subjectOptions = INDIAN_SUBJECTS.map(subject => ({
  value: subject,
  label: subject
}))
```

## Templates

### Lesson Plan Template
Comprehensive template for multi-grade lesson planning with:
- Learning objectives by grade level
- Materials and resources
- Structured lesson flow
- Assessment strategies
- Cultural relevance

### Worksheet Template
Student worksheet generation with:
- Age-appropriate questions
- Mixed question types
- Visual elements
- Answer keys
- Printable format

### Assessment Template
Multi-faceted assessment creation:
- Formative and summative assessments
- Rubrics and grading criteria
- Practical evaluations
- Peer and self-assessment

## Constants

### Education System
- NCF (National Curriculum Framework) subjects
- Grade-wise subject mappings
- Regional language support
- Learning objectives taxonomy

### Technical Configuration
- Firebase collection naming
- AI model identifiers
- API response structures
- Error handling formats

## Utilities

### Validation
- Grade level validation (1-12)
- Subject validation against NCF
- Lesson plan data structure validation
- Input sanitization

### Text Processing
- Reading level estimation
- Content cleaning and formatting
- Language detection (English/Hindi)
- Section extraction from generated content

### Localization
- Indian date formatting (DD/MM/YYYY)
- Currency formatting (₹)
- Regional language detection
- Cultural context awareness

## Best Practices

1. **Consistency**: Use shared constants across all components
2. **Validation**: Always validate input data using utility functions
3. **Formatting**: Use standard response formats for APIs
4. **Localization**: Consider Indian context in all content
5. **Accessibility**: Ensure templates work with limited resources

## Contributing

When adding new shared resources:
1. Follow existing naming conventions
2. Add appropriate documentation
3. Include validation where needed
4. Consider both frontend and backend usage
5. Test with rural education context
