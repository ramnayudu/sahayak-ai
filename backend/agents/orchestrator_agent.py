"""
Orchestrator Agent for Sahayak AI agent framework.
This agent coordinates the work of sub-agents based on user requests.
"""

from typing import Dict, List, Optional, Any, Union
import json
import re
import uuid
from .base_agent import BaseAgent, AgentType, MessageType, AgentMessage

class OrchestratorAgent(BaseAgent):
    """
    Main orchestrator agent that coordinates the work of sub-agents.
    This agent receives user requests, determines which sub-agents to invoke,
    and coordinates their responses into a cohesive output.
    """
    
    def __init__(self, vertex_ai_service):
        """Initialize the orchestrator agent"""
        super().__init__("orchestrator", AgentType.ORCHESTRATOR)
        self.vertex_ai_service = vertex_ai_service
        self.sub_agents = {}
        
    def register_agent(self, agent: BaseAgent):
        """Register a sub-agent with the orchestrator"""
        self.sub_agents[agent.agent_id] = agent
        
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process a message received from a sub-agent"""
        if message.message_type == MessageType.RESPONSE:
            # Store the response in the conversation history
            self.conversation_history.append(message)
            
            # Check if we have responses from all sub-agents for this conversation
            if self._check_all_responses_received(message.conversation_id):
                # Combine the responses and send back to the user
                return self._combine_responses(message.conversation_id)
        
        return None
    
    def _check_all_responses_received(self, conversation_id: str) -> bool:
        """Check if all sub-agents have responded for a given conversation"""
        # Get all messages for this conversation
        conversation_messages = [
            msg for msg in self.conversation_history 
            if msg.conversation_id == conversation_id
        ]
        
        # Get all request messages sent by the orchestrator
        request_messages = [
            msg for msg in conversation_messages 
            if msg.sender == self.agent_id and msg.message_type == MessageType.REQUEST
        ]
        
        # Get all response messages received by the orchestrator
        response_messages = [
            msg for msg in conversation_messages 
            if msg.receiver == self.agent_id and msg.message_type == MessageType.RESPONSE
        ]
        
        # Check if we have a response for each request
        return len(response_messages) == len(request_messages)
    
    def _combine_responses(self, conversation_id: str) -> AgentMessage:
        """Combine responses from all sub-agents into a cohesive output"""
        # Get all response messages for this conversation
        response_messages = [
            msg for msg in self.conversation_history 
            if msg.conversation_id == conversation_id 
            and msg.receiver == self.agent_id 
            and msg.message_type == MessageType.RESPONSE
        ]
        
        # Combine the responses
        combined_content = {}
        for msg in response_messages:
            agent_type = msg.sender.split("-")[0]  # Extract agent type from agent_id
            combined_content[agent_type] = msg.content
        
        # Create a response message
        response = self.create_message(
            receiver="user",
            message_type=MessageType.RESPONSE,
            content=combined_content,
            conversation_id=conversation_id
        )
        
        return response
    
    async def analyze_user_request(self, user_request: str) -> Dict[str, bool]:
        """
        Analyze the user request to determine which sub-agents to invoke.
        Returns a dictionary with agent types as keys and boolean values indicating
        whether each agent should be invoked.
        """
        # Use Vertex AI to analyze the request
        prompt = f"""
        Analyze the following user request and determine which specialized agents should be invoked.
        
        User request: "{user_request}"
        
        For each agent type, respond with "true" if the agent should be invoked, or "false" if not.
        
        1. Lesson Creator: Should create educational content and lesson plans.
        2. Image Generator: Should create visual aids and illustrations.
        3. Assignment Creator: Should create assignments, worksheets, and assessments.
        4. Translator: Should translate content to another language (only if a specific non-English language is requested).
        
        Format your response as a JSON object with the following structure:
        {{
            "lesson_creator": true/false,
            "image_generator": true/false,
            "assignment_creator": true/false,
            "translator": true/false,
            "target_language": "language_name" (if translator is true, otherwise null)
        }}
        """
        
        response = await self.vertex_ai_service.generate_text(prompt)
        
        # Extract JSON from the response
        json_match = re.search(r'({.*})', response, re.DOTALL)
        if json_match:
            try:
                analysis = json.loads(json_match.group(1))
                return analysis
            except json.JSONDecodeError:
                # Fallback to default analysis if JSON parsing fails
                pass
        
        # Default analysis if extraction fails
        return {
            "lesson_creator": True,
            "image_generator": "image" in user_request.lower() or "visual" in user_request.lower(),
            "assignment_creator": "assignment" in user_request.lower() or "worksheet" in user_request.lower(),
            "translator": any(lang.lower() in user_request.lower() for lang in ["translate", "hindi", "telugu", "tamil", "bengali"]),
            "target_language": self._extract_language(user_request)
        }
    
    def _extract_language(self, text: str) -> Optional[str]:
        """Extract the target language from the user request"""
        languages = ["hindi", "telugu", "tamil", "bengali", "marathi", "gujarati", 
                    "kannada", "malayalam", "punjabi", "urdu", "odia", "assamese"]
        
        for lang in languages:
            if lang.lower() in text.lower():
                return lang.capitalize()
        
        return None
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the orchestrator agent with the given input data"""
        user_request = input_data.get("user_request", "")
        
        # Create a new conversation ID
        conversation_id = str(uuid.uuid4())
        
        # Analyze the user request
        analysis = await self.analyze_user_request(user_request)
        
        # Determine which sub-agents to invoke
        agents_to_invoke = []
        if analysis.get("lesson_creator", False):
            agents_to_invoke.append("lesson_creator")
        if analysis.get("image_generator", False):
            agents_to_invoke.append("image_generator")
        if analysis.get("assignment_creator", False):
            agents_to_invoke.append("assignment_creator")
        if analysis.get("translator", False):
            agents_to_invoke.append("translator")
        
        # Prepare the request for each sub-agent
        for agent_type in agents_to_invoke:
            agent_id = f"{agent_type}-{uuid.uuid4()}"
            if agent_type in self.sub_agents:
                agent = self.sub_agents[agent_type]
                
                # Create agent-specific content
                content = {
                    "user_request": user_request,
                    "analysis": analysis
                }
                
                # Add target language for translator agent
                if agent_type == "translator" and analysis.get("target_language"):
                    content["target_language"] = analysis.get("target_language")
                
                # Create and send message to the sub-agent
                message = self.create_message(
                    receiver=agent.agent_id,
                    message_type=MessageType.REQUEST,
                    content=content,
                    conversation_id=conversation_id
                )
                
                # Send the message to the sub-agent
                response = agent.process_message(message)
                if response:
                    self.process_message(response)
        
        # Return a status message
        return {
            "status": "processing",
            "conversation_id": conversation_id,
            "agents_invoked": agents_to_invoke
        }