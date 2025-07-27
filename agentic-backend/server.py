#!/usr/bin/env python3
"""
FastAPI server to expose the Sahayak ADK root agent as a REST API.
This server runs the agent locally and provides endpoints for interaction.
"""

import os
import asyncio
from typing import Any, Dict, Optional, AsyncGenerator
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
import json

# Load environment variables
load_dotenv()

# Import the root agent
from sahayakai.agent import root_agent

app = FastAPI(
    title="Sahayak AI Agent Server",
    description="REST API for the Sahayak ADK Root Agent",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    stream: bool = False

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    status: str = "success"

class HealthResponse(BaseModel):
    status: str
    agent_name: str
    model: str

# Global conversation storage (in production, use a proper database)
conversations: Dict[str, list] = {}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        agent_name=root_agent.name,
        model=str(root_agent.model)  # Convert to string to handle BaseLlm types
    )

async def invoke_agent(message: str, conversation_id: str) -> str:
    """
    Invoke the ADK agent with a simplified approach.
    This is a placeholder implementation - you'll need to implement proper ADK integration.
    """
    try:
        # For now, return a mock response that indicates the system is working
        # This should be replaced with proper ADK agent invocation once the integration is complete
        
        # Simulate agent processing based on the message content
        if "lesson" in message.lower() or "teach" in message.lower():
            return f"""
**Generated Lesson Content for: {message}**

**Subject Analysis**: The request appears to be about educational content creation.

**Content Generated**:
- Lesson plan structure created
- Learning objectives identified  
- Age-appropriate activities suggested
- Assessment methods included

**Agents Invoked**: 
- Content Generation Agent: Created structured lesson materials
- Visual Aid Agent: Prepared to generate supporting images
- Worksheet Agent: Ready to create practice exercises

**Note**: This is a demo response from the Sahayak ADK Agent System. The full agent integration is in development.

**Next Steps**: The teacher can now review and customize this content for their multi-grade classroom.
"""
        
        elif "image" in message.lower() or "visual" in message.lower():
            return f"""
**Visual Aid Generation for: {message}**

**Image Generation Request Processed**:
- Educational imagery concepts identified
- Cultural appropriateness verified
- Age-group suitability confirmed

**Generated Visual Aids**:
- Diagrams and illustrations prepared
- Interactive visual elements suggested
- Culturally relevant imagery selected

**Status**: Visual aid agent has processed your request. Images would be generated using the integrated Imagen model.

**Agent Details**: Visual Aid Agent specialized for rural Indian classroom contexts.
"""
        
        else:
            return f"""
**Sahayak AI Agent Response for: {message}**

**Analysis**: Your request has been processed by the Sahayak multi-agent system.

**Agent Processing**:
- Request analyzed and categorized
- Appropriate sub-agents identified
- Content generation pipeline activated
- Multi-language support enabled

**Available Capabilities**:
- Lesson plan creation
- Visual aid generation  
- Worksheet development
- Story creation
- Multi-language translation

**Status**: Ready to assist with your educational content needs.

**Note**: This demonstrates the Sahayak ADK agent system. Full integration with Google ADK is in progress.
"""
        
    except Exception as e:
        return f"Agent processing error: {str(e)}. Please try again."

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Send a message to the Sahayak agent and get a response.
    """
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or f"conv_{len(conversations)}"
        
        # Initialize conversation if new
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        # Add user message to conversation
        conversations[conversation_id].append({
            "role": "user",
            "content": request.message
        })
        
        # Invoke the agent
        agent_response = await invoke_agent(request.message, conversation_id)
        
        # Add agent response to conversation
        conversations[conversation_id].append({
            "role": "assistant", 
            "content": agent_response
        })
        
        return ChatResponse(
            response=agent_response,
            conversation_id=conversation_id,
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

async def stream_agent_response(message: str, conversation_id: str) -> AsyncGenerator[str, None]:
    """Stream agent response for real-time interaction."""
    try:
        # Get the full response
        full_response = await invoke_agent(message, conversation_id)
        
        # Stream it word by word for demonstration
        words = full_response.split()
        for i, word in enumerate(words):
            chunk = word + " "
            yield f"data: {json.dumps({'chunk': chunk, 'conversation_id': conversation_id})}\n\n"
            await asyncio.sleep(0.1)  # Small delay for streaming effect
        
        yield f"data: {json.dumps({'done': True, 'conversation_id': conversation_id})}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e), 'conversation_id': conversation_id})}\n\n"

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream chat responses from the agent."""
    conversation_id = request.conversation_id or f"conv_{len(conversations)}"
    
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    
    conversations[conversation_id].append({
        "role": "user",
        "content": request.message
    })
    
    return StreamingResponse(
        stream_agent_response(request.message, conversation_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "conversation_id": conversation_id,
        "messages": conversations[conversation_id]
    }

@app.get("/conversations")
async def list_conversations():
    """List all conversation IDs"""
    return {
        "conversations": list(conversations.keys()),
        "count": len(conversations)
    }

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    del conversations[conversation_id]
    return {"message": f"Conversation {conversation_id} deleted"}

@app.get("/agent-info")
async def get_agent_info():
    """Get detailed information about the agent"""
    return {
        "agent_name": root_agent.name,
        "model": str(root_agent.model),
        "description": "Sahayak AI - Multi-agent system for rural classroom education",
        "capabilities": [
            "Lesson plan generation",
            "Visual aid creation", 
            "Worksheet development",
            "Story generation",
            "Multi-language support",
            "Cultural adaptation for Indian classrooms"
        ],
        "sub_agents": [
            "Content Generation Agent",
            "Visual Aid Agent", 
            "Story Agent",
            "Worksheet Agent",
            "Merger Agent"
        ],
        "supported_languages": [
            "English",
            "Hindi", 
            "Telugu",
            "Tamil",
            "Bengali",
            "Marathi",
            "Gujarati"
        ]
    }

@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "name": "Sahayak AI Agent Server",
        "status": "running",
        "agent": root_agent.name,
        "description": "ADK-powered educational assistant for rural multi-grade classrooms",
        "endpoints": [
            "/health",
            "/chat",
            "/chat/stream", 
            "/conversations",
            "/agent-info",
            "/docs"
        ]
    }

if __name__ == "__main__":
    # Configure the server
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print(f"Starting Sahayak AI Agent Server on {host}:{port}")
    print(f"Agent: {root_agent.name}")
    print(f"Model: {str(root_agent.model)}")
    print(f"API Documentation: http://{host}:{port}/docs")
    
    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
