

from google.adk.agents import Agent
from .tools import generate_images
from ... import config

from . import prompt

# Use local model if configured, otherwise use cloud model
model_name = config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else 'gemini-2.0-flash-exp'

visual_aid_agent = Agent(
    name='visual_aid_agent',
    model=model_name,
    instruction=prompt.IMAGEGEN_PROMPT,
    description=("You are an expert in creating images with imagen 3"),
    tools=[generate_images],
    output_key="output_image"
)
