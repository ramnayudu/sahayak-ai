

from google.adk.agents import Agent

from ..story_agent import story_agent
from ..worksheet_agent import worksheet_agent

from . import prompt


orchestrator_agent = Agent(
    model='gemini-2.0-flash-exp',
    name='orchestrator_agent',
    description='Intelligent task distribution manager that analyzes teacher requests and routes to appropriate specialist agents (story, worksheet, visual aid) based on content requirements',
    # The ParallelAgent is a structural agent that runs its sub-agents in parallel.
    # It does not take `model` or `instruction` parameters itself.
    sub_agents=[story_agent, worksheet_agent],
    instruction=prompt.ORCHESTRATOR_PROMPT
)
    