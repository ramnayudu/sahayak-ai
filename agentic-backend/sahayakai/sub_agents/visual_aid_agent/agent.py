

from google.adk.agents import Agent
from .tools import generate_images

from . import prompt


visual_aid_agent = Agent(
    name='visual_aid_agent',
    model='gemini-2.0-flash-exp',
    instruction=prompt.IMAGEGEN_PROMPT,
    description=("You are an expert in creating images with imagen 3"),
    tools=[generate_images],
    output_key="output_image"
)
