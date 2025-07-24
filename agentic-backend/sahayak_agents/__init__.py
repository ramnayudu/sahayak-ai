"""Sahayak Agents package - AI co-teacher for rural classrooms."""

from .agent import SahayakOrchestratorAgent
from .sub_agents.story_agent import StoryAgent
from .sub_agents.worksheet_agent import WorksheetAgent
from .sub_agents.visual_aid_agent import VisualAidAgent

__version__ = "0.1.0"

__all__ = [
    "SahayakOrchestratorAgent",
    "StoryAgent", 
    "WorksheetAgent",
    "VisualAidAgent"
]
