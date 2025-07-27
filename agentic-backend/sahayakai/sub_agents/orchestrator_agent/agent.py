

from google.adk.agents import Agent

from ..story_agent import story_agent
from ..worksheet_agent import worksheet_agent
from ... import config

from . import prompt

# Use local model if configured, otherwise use cloud model
model_name = config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else 'gemini-2.0-flash-exp'

orchestrator_agent = Agent(
    model=model_name,
    name='orchestrator_agent',
    description='Intelligent task distribution manager that analyzes teacher requests and routes to appropriate specialist agents (story, worksheet, visual aid) based on content requirements',
    # The ParallelAgent is a structural agent that runs its sub-agents in parallel.
    # It does not take `model` or `instruction` parameters itself.
    sub_agents=[story_agent, worksheet_agent],
    instruction=prompt.ORCHESTRATOR_PROMPT
)
    