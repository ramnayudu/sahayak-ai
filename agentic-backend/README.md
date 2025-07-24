# Sahayak AI - Agentic Backend

An AI-powered co-teacher system designed for rural multi-grade classrooms in India, built using Google's Agent Development Kit (ADK).

## Features

- **Multi-agent Architecture**: Orchestrator agent coordinates specialized sub-agents
- **Multilingual Support**: English, Hindi, Telugu, and more
- **Educational Focus**: Stories, worksheets, and visual aids for rural classrooms
- **Model Selection**: Gemini for rich content, Gemma for structured tasks

## Agents

1. **Orchestrator Agent**: Routes tasks to appropriate sub-agents
2. **Story Agent**: Generates local-language, age-appropriate stories
3. **Worksheet Agent**: Creates differentiated practice questions
4. **Visual Aid Agent**: Produces prompts for educational diagrams

## Setup

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your Google Cloud credentials
   ```

3. Run the API server:
   ```bash
   poetry run python api/main.py
   ```

## API Endpoints

- `POST /generate`: Generate educational content
- `GET /health`: Health check

## Development

- Run tests: `poetry run pytest`
- Format code: `poetry run black .`
- Sort imports: `poetry run isort .`
