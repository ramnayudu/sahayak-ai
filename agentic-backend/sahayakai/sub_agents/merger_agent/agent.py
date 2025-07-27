

from google.adk.agents import Agent
from ... import config

from . import prompt

# Use local model if configured, otherwise use cloud model
model_name = config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else 'gemini-2.0-flash-exp'

merger_agent = Agent(
    name='merger_agent',
    model=model_name,
    instruction=prompt.MERGER_PROMPT,
    description="Content Integration Specialist that combines outputs from Story Agent, Worksheet Agent, and Visual Aid Agent into unified, teacher-ready lesson packages for rural Indian multi-grade classrooms. Ensures pedagogical alignment, cultural consistency, and practical implementation guidance."
)

root_agent = merger_agent
