
from google.adk import Agent
from ... import config

from . import prompt

# Use local model if configured, otherwise use cloud model
model_name = config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else 'gemini-2.0-flash'

worksheet_agent = Agent(
    model=model_name,
    name='worksheet_agent',
    description='Creates age-appropriate, subject-relevant practice worksheets in simple, culturally aware format for rural Indian multi-grade classrooms',
    instruction=prompt.WORKSHEET_PROMPT,
)
