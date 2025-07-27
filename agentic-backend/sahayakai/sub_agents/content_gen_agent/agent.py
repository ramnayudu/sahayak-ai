

from google.adk.agents import Agent
from ... import config

from . import prompt

# Use local model if configured, otherwise use cloud model
model_name = config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else 'gemini-2.0-flash-exp'

content_gen_agent = Agent(
    name='content_gen_agent',
    model=model_name,
    instruction=prompt.CONTENT_GEN_PROMPT,
    description="""ContentGenAgent is a unified, intelligent content-generation agent in the Sahayak agentic system. It handles teacher requests related to lesson materials including stories, worksheets, Q&A explanations, and lesson plans.
It supports multiple Indian languages, dynamically adjusts to grade level, and ensures cultural and contextual relevance for rural classrooms."""
)
