

from google.adk.agents import Agent

from . import prompt


content_gen_agent = Agent(
    name='content_gen_agent',
    model='gemini-2.0-flash-exp',
    instruction=prompt.CONTENT_GEN_PROMPT,
    description="""ContentGenAgent is a unified, intelligent content-generation agent in the Sahayak agentic system. It handles teacher requests related to lesson materials including stories, worksheets, Q&A explanations, and lesson plans.
It supports multiple Indian languages, dynamically adjusts to grade level, and ensures cultural and contextual relevance for rural classrooms."""
)
