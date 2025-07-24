"""
Base Agent class and A2A protocol definition for Sahayak AI agent framework.
This module defines the base agent class and the protocol for agent-to-agent communication.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
import json
import uuid
from datetime import datetime

# A2A Protocol Message Types
class MessageType(str, Enum):
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"
    INFO = "info"

# A2A Protocol Message
class AgentMessage(BaseModel):
    """Message format for agent-to-agent communication"""
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    sender: str
    receiver: str
    message_type: MessageType
    content: Dict[str, Any]
    conversation_id: Optional[str] = None
    parent_message_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

# Agent Types
class AgentType(str, Enum):
    ORCHESTRATOR = "orchestrator"
    LESSON_CREATOR = "lesson_creator"
    IMAGE_GENERATOR = "image_generator"
    ASSIGNMENT_CREATOR = "assignment_creator"
    TRANSLATOR = "translator"

# Base Agent Class
class BaseAgent(ABC):
    """Base class for all agents in the Sahayak AI agent framework"""
    
    def __init__(self, agent_id: str, agent_type: AgentType):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.conversation_history: List[AgentMessage] = []
    
    def create_message(
        self, 
        receiver: str, 
        message_type: MessageType, 
        content: Dict[str, Any],
        conversation_id: Optional[str] = None,
        parent_message_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AgentMessage:
        """Create a new message to send to another agent"""
        if metadata is None:
            metadata = {}
            
        message = AgentMessage(
            sender=self.agent_id,
            receiver=receiver,
            message_type=message_type,
            content=content,
            conversation_id=conversation_id,
            parent_message_id=parent_message_id,
            metadata=metadata
        )
        
        return message
    
    def send_message(self, message: AgentMessage) -> None:
        """Send a message to another agent"""
        # Add message to conversation history
        self.conversation_history.append(message)
        
        # In a real implementation, this would send the message to the receiver
        # For now, we'll just log it
        print(f"Message sent from {message.sender} to {message.receiver}")
        
        # Process the message
        return self.process_message(message)
    
    @abstractmethod
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process a received message and optionally return a response"""
        pass
    
    @abstractmethod
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent with the given input data"""
        pass