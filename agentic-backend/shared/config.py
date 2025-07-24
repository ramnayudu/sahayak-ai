"""Configuration settings for Sahayak agents."""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    """Model configuration for different task types."""
    gemini_model: str = "gemini-1.5-pro"
    gemma_model: str = "gemma-2-9b-it"
    max_tokens: int = 2048
    temperature: float = 0.7


@dataclass
class LanguageConfig:
    """Language configuration."""
    default_language: str = "en"
    supported_languages: List[str] = field(default_factory=lambda: ["en", "hi", "te"])
class Config:
    """Main configuration class."""
    
    def __init__(self):
        self.google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.vertex_ai_location = os.getenv("VERTEX_AI_LOCATION", "us-central1")
        self.model = ModelConfig(
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-1.5-pro"),
            gemma_model=os.getenv("GEMMA_MODEL", "gemma-2-9b-it"),
            max_tokens=int(os.getenv("MAX_TOKENS", "2048")),
            temperature=float(os.getenv("TEMPERATURE", "0.7"))
        )
        self.language = LanguageConfig(
            default_language=os.getenv("DEFAULT_LANGUAGE", "en"),
            supported_languages=os.getenv("SUPPORTED_LANGUAGES", "en,hi,te").split(",")
        )
    
    def get_model_for_task(self, task_type: str) -> str:
        """Select appropriate model based on task type."""
        rich_content_tasks = ["story", "visual_aid"]
        if task_type in rich_content_tasks:
            return self.model.gemini_model
        return self.model.gemma_model


# Global configuration instance
config = Config()
