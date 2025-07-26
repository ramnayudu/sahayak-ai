
from google.adk import Agent

from . import prompt

story_agent = Agent(
    model='gemini-2.0-flash',
    name='story_agent',
    description='Generates short, age-appropriate, culturally relevant educational stories for rural Indian multi-grade classrooms in the teacher\'s preferred language',
    instruction=prompt.STORY_PROMPT,
)
