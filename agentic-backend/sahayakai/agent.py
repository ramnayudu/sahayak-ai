

from google.adk.agents import Agent
from google.genai import types
from .sub_agents.orchestrator_agent import orchestrator_agent
from .sub_agents.merger_agent import merger_agent

from . import prompt, config
from .tools import call_content_gen_agent , call_visual_aid_agent


# Create the main workflow with orchestrator and merger
#sahayak_agent = SequentialAgent(
  #  name='sahayak_agent',
   # description= prompt.SAHAYAK_PROMPT,
    #sub_agents=[orchestrator_agent, merger_agent],
#)

# Use local model if configured, otherwise use cloud model
model_name = config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else 'gemini-2.0-flash-exp'

root_agent = Agent(
    model=model_name,
    name="sahayak_agent",
    instruction=prompt.SAHAYAK_PROMPT,
    global_instruction=(
        f"""
        You are part of the **Sahayak Agentic System**, a multilingual AI assistant designed to help teachers in rural, multi-grade classrooms across India.
        """
    ),
    #sub_agents=[merger_agent],
    tools=[
        call_content_gen_agent,
        call_visual_aid_agent
    ],
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)
