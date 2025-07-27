
from google.adk import Agent
from ... import config

from . import prompt

# Use local model if configured, otherwise use cloud model
model_name = config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else 'gemini-2.0-flash'

story_agent = Agent(
    model=model_name,
    name='story_agent',
    description='Generates short, age-appropriate, culturally relevant educational stories for rural Indian multi-grade classrooms in the teacher\'s preferred language',
    instruction=prompt.STORY_PROMPT,
)
