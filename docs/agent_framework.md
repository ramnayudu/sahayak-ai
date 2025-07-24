# Agent Framework Documentation

## Overview

The Sahayak AI project implements an agent-based framework using the Agent Development Kit (ADK) and Agent-to-Agent (A2A) protocol. This framework enables a modular, extensible approach to AI-powered content generation for educational purposes.

The framework consists of a main orchestrator agent that coordinates the work of specialized sub-agents:

1. **Lesson Creation Agent**: Generates educational content and lesson plans
2. **Image Generation Agent**: Creates visual aids and illustrations
3. **Assignment Creation Agent**: Produces worksheets, assignments, and assessments
4. **Language Translation Agent**: Translates content to regional Indian languages

## Architecture

### Base Components

- **BaseAgent**: Abstract base class that all agents inherit from
- **AgentMessage**: Message format for agent-to-agent communication
- **MessageType**: Enum for different types of messages (request, response, error, info)
- **AgentType**: Enum for different types of agents

### Agent Communication

Agents communicate using a standardized message format that includes:
- Message ID
- Timestamp
- Sender and receiver IDs
- Message type
- Content
- Conversation ID
- Parent message ID
- Metadata

This enables asynchronous, multi-step conversations between agents.

## Agent Descriptions

### Orchestrator Agent

The main agent that:
- Analyzes user requests to determine which sub-agents to invoke
- Coordinates the work of sub-agents
- Combines responses from sub-agents into a cohesive output

```python
# Example usage
orchestrator = OrchestratorAgent(vertex_ai_service)
result = await orchestrator.run({"user_request": "generate class material on fractions for 4th graders in Telugu"})
```

### Lesson Creation Agent

Specialized agent that:
- Generates comprehensive lesson plans
- Extracts subject, topic, and grade information from requests
- Creates structured educational content with learning objectives, materials, activities, etc.

```python
# Example usage
lesson_agent = LessonCreationAgent(vertex_ai_service)
result = await lesson_agent.run({
    "user_request": "lesson plan for fractions",
    "subject": "Mathematics",
    "topic": "Fractions",
    "grades": [4],
    "duration": 45
})
```

### Image Generation Agent

Specialized agent that:
- Creates visual aids and illustrations for educational content
- Generates image prompts and descriptions
- Provides materials lists and creation steps for physical visual aids

```python
# Example usage
image_agent = ImageGenerationAgent(vertex_ai_service)
result = await image_agent.run({
    "user_request": "visual aids for fractions",
    "subject": "Mathematics",
    "topic": "Fractions",
    "grade": 4
})
```

### Assignment Creation Agent

Specialized agent that:
- Creates worksheets with questions and answer keys
- Generates comprehensive assessments with different question types
- Produces rubrics for grading

```python
# Example usage
assignment_agent = AssignmentCreationAgent(vertex_ai_service)
result = await assignment_agent.run({
    "user_request": "worksheet on fractions",
    "subject": "Mathematics",
    "topic": "Fractions",
    "grade": 4
})
```

### Language Translation Agent

Specialized agent that:
- Translates educational content to regional Indian languages
- Preserves formatting and structure of the original content
- Adapts examples to be culturally relevant

```python
# Example usage
translation_agent = LanguageTranslationAgent(vertex_ai_service)
result = await translation_agent.run({
    "user_request": "translate to Telugu",
    "target_language": "Telugu",
    "content": {...}  # Content to translate
})
```

## API Endpoints

The agent framework is exposed through the following API endpoints:

### `/generate-with-agents`

Main endpoint that uses the orchestrator agent to coordinate all sub-agents.

**Request:**
```json
{
  "user_request": "generate class material and assignment on fractions for 4th graders in Telugu",
  "mode": "online"
}
```

**Response:**
```json
{
  "content": {
    "status": "processing",
    "conversation_id": "...",
    "agents_invoked": ["lesson_creator", "image_generator", "assignment_creator", "translator"]
  },
  "conversation_id": "...",
  "status": "processing",
  "generated_at": "2025-07-23T23:00:00",
  "mode_used": "online"
}
```

### Individual Agent Endpoints

Each agent also has its own endpoint:

- `/generate-lesson-plan`: Uses the lesson creation agent
- `/generate-worksheet`: Uses the assignment creation agent for worksheets
- `/generate-visual-aid`: Uses the image generation agent
- `/assess-student`: Uses the assignment creation agent for assessments

## Prompt Templates

The agent framework uses specialized prompt templates for each agent:

- **Orchestrator Templates**:
  - `ORCHESTRATOR_ANALYSIS_TEMPLATE`: For analyzing user requests
  - `ORCHESTRATOR_COMBINE_TEMPLATE`: For combining agent responses

- **Agent-Specific Templates**:
  - `LESSON_PLAN_TEMPLATE`: For generating lesson plans
  - `WORKSHEET_TEMPLATE`: For creating worksheets
  - `VISUAL_AID_TEMPLATE`: For generating visual aids
  - `ASSESSMENT_TEMPLATE`: For creating assessments
  - `TRANSLATION_TEMPLATE`: For translating content

## Testing

A test script is provided to test the agent framework:

```bash
# Run the test script
python backend/test_agents.py
```

This script tests the example scenario of generating class material and assignment on fractions for 4th graders in Telugu.

## Future Enhancements

Planned enhancements to the agent framework include:

1. **Improved Agent Coordination**: Enhanced orchestration with better dependency management
2. **Memory and Context**: Persistent memory for agents to improve context awareness
3. **Feedback Loop**: Incorporating user feedback to improve agent responses
4. **Offline Mode**: Support for running agents with local models via Ollama
5. **Additional Specialized Agents**: New agents for specific educational needs