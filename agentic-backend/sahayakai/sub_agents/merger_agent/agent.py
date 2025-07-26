

from google.adk.agents import Agent

from . import prompt


merger_agent = Agent(
    name='merger_agent',
    model='gemini-2.0-flash-exp',
    instruction=prompt.MERGER_PROMPT,
    description="Content Integration Specialist that combines outputs from Story Agent, Worksheet Agent, and Visual Aid Agent into unified, teacher-ready lesson packages for rural Indian multi-grade classrooms. Ensures pedagogical alignment, cultural consistency, and practical implementation guidance."
)

root_agent = merger_agent
