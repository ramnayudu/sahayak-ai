# Sahayak AI - Agentic Backend

## Project Structure

```
agentic-backend/
├── sahayak_agents/           # Main agent package
│   ├── __init__.py
│   ├── agent.py             # Orchestrator agent
│   └── sub_agents/          # Specialized agents
│       ├── __init__.py
│       ├── story_agent.py   # Story generation
│       ├── worksheet_agent.py # Worksheet creation
│       └── visual_aid_agent.py # Visual aid design
├── shared/                  # Shared utilities
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── prompts.py          # Prompt templates
│   └── utils.py            # Utility functions
├── api/                    # FastAPI backend
│   └── main.py            # API server
├── pyproject.toml         # Poetry configuration
├── .env.example          # Environment template
├── test_system.py        # System tests
└── README.md            # This file
```

## Architecture Overview

The Sahayak AI system uses a **multi-agent architecture** built with Google's Agent Development Kit (ADK):

### Core Components

1. **Orchestrator Agent** (`SahayakOrchestratorAgent`)
   - Routes tasks to appropriate sub-agents
   - Analyzes user input and creates structured requests
   - Provides system-wide capabilities and suggestions

2. **Story Agent** (`StoryAgent`)
   - Generates educational stories in local languages
   - Creates age-appropriate content with moral lessons
   - Uses Gemini for rich, narrative content

3. **Worksheet Agent** (`WorksheetAgent`)
   - Creates differentiated practice exercises
   - Generates multi-level questions for mixed-grade classrooms
   - Uses Gemma for structured, educational content

4. **Visual Aid Agent** (`VisualAidAgent`)
   - Designs simple educational diagrams
   - Provides step-by-step drawing instructions
   - Creates materials suitable for rural classrooms

### Model Selection Strategy

- **Gemini**: Used for rich, creative content (stories, visual aids)
- **Gemma**: Used for structured, lightweight tasks (worksheets, routing)

## API Endpoints

### Core Endpoints

- `POST /generate` - Generate educational content
- `POST /analyze` - Analyze user input and create task requests
- `GET /capabilities` - Get system capabilities
- `POST /suggest` - Get suggestions for incomplete requests

### Utility Endpoints

- `GET /health` - Health check
- `GET /tasks/{task_type}/template` - Get example templates
- `GET /languages` - Get supported languages

## Usage Examples

### 1. Generate a Story

```json
POST /generate
{
  "task_type": "story",
  "topic": "importance of trees",
  "grade_level": "3-5",
  "subject": "environmental science",
  "language": "hi",
  "context": "rural village setting"
}
```

### 2. Create a Worksheet

```json
POST /generate
{
  "task_type": "worksheet", 
  "topic": "multiplication tables",
  "grade_level": "2-4",
  "subject": "mathematics",
  "language": "en",
  "additional_params": {
    "skills": "basic multiplication, problem solving"
  }
}
```

### 3. Design a Visual Aid

```json
POST /generate
{
  "task_type": "visual_aid",
  "topic": "parts of a plant",
  "grade_level": "4-6", 
  "subject": "science",
  "language": "te",
  "additional_params": {
    "objective": "identify and label plant parts"
  }
}
```

### 4. Analyze Natural Language Input

```json
POST /analyze
{
  "user_input": "I need a Hindi story about sharing for grade 2 students",
  "language": "hi"
}
```

## Key Features

### Multilingual Support
- **English**: Primary interface language
- **Hindi**: हिंदी भाषा समर्थन
- **Telugu**: తెలుగు భాష మద్దతు

### Rural Classroom Optimization
- Content designed for low-resource environments
- Materials using locally available supplies
- Cultural sensitivity and local context integration
- Multi-grade classroom support

### Differentiated Learning
- Automatic content adaptation for different grade levels
- Multiple difficulty levels in worksheets
- Age-appropriate language and complexity
- Visual, auditory, and kinesthetic learning styles

## Installation & Setup

### Prerequisites
- Python 3.11+
- Poetry (dependency management)
- Google Cloud Account
- ADK Python library

### Setup Steps

1. **Install Dependencies**
   ```bash
   cd agentic-backend
   poetry install
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Set Google Cloud Credentials**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   ```

4. **Test the System**
   ```bash
   poetry run python test_system.py
   ```

5. **Run API Server**
   ```bash
   poetry run python api/main.py
   ```

## Environment Variables

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
VERTEX_AI_LOCATION=us-central1

# Model Configuration  
GEMINI_MODEL=gemini-1.5-pro
GEMMA_MODEL=gemma-2-9b-it

# Language & Behavior
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,hi,te
MAX_TOKENS=2048
TEMPERATURE=0.7
```

## Development Guidelines

### Adding New Agent Types

1. Create agent class in `sahayak_agents/sub_agents/`
2. Add system prompts in `shared/prompts.py`
3. Update orchestrator routing in `agent.py`
4. Add API endpoints in `api/main.py`
5. Update capabilities in orchestrator

### Prompt Engineering Best Practices

- Include cultural context and rural settings
- Specify grade-appropriate language
- Provide clear structure and format expectations
- Include examples and edge case handling
- Test with multiple languages

### Testing Strategy

- Unit tests for utilities (`shared/utils.py`)
- Integration tests for agents
- API endpoint testing
- Multilingual content validation
- Rural context appropriateness review

## Integration with Existing System

This agentic backend complements the existing Sahayak system:

- **Frontend**: Connects to existing React frontend
- **Backend**: Runs on port 8001 (existing backend on 8000)
- **Database**: Can share Firebase/database with existing system
- **Authentication**: Integrate with existing auth system

## Cultural Considerations

### Rural Indian Context
- Use familiar agricultural examples
- Reference local festivals and traditions
- Include joint family structures
- Consider seasonal cycles and rural occupations

### Language Implementation
- Script-aware content generation
- Cultural idioms and expressions
- Regional variations and dialects
- Code-mixing (Hindi-English) support

## Future Enhancements

1. **Audio Support**: Text-to-speech for story narration
2. **Image Generation**: Simple diagrams and illustrations
3. **Assessment Tools**: Automated grading and feedback
4. **Parent Communication**: Home learning materials
5. **Offline Capability**: Content caching and offline operation
6. **Regional Languages**: Expand to more Indian languages

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure Python path includes project root
2. **Model Access**: Verify Google Cloud credentials and permissions
3. **Language Issues**: Check script encoding and language detection
4. **Memory Issues**: Adjust MAX_TOKENS for large content generation

### Debug Mode

```bash
export SAHAYAK_DEBUG=true
poetry run python api/main.py
```

## Contributing

1. Follow existing code structure and naming conventions
2. Add comprehensive docstrings and type hints
3. Test multilingual functionality
4. Validate rural classroom appropriateness
5. Update documentation for new features

## License

This project is part of the Sahayak AI educational initiative for rural Indian classrooms.
