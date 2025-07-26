
from google.adk import Agent

from . import prompt

worksheet_agent = Agent(
    model='gemini-2.0-flash',
    name='worksheet_agent',
    description='Creates age-appropriate, subject-relevant practice worksheets in simple, culturally aware format for rural Indian multi-grade classrooms',
    instruction=prompt.WORKSHEET_PROMPT,
)
