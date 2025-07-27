#!/usr/bin/env python3
"""
Local Development Server for Sahayak AI
This server allows testing the agents locally with Transformer Lab
"""

import asyncio
import json
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn

from sahayakai.local_model_client import TransformerLabClient
from sahayakai import config

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Sahayak AI Local Development Server",
    description="Local development server using Transformer Lab",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize local client
if config.USE_LOCAL_MODEL:
    local_client = TransformerLabClient()
else:
    local_client = None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    max_tokens: int = 256
    temperature: float = 0.7

class AgentRequest(BaseModel):
    message: str
    agent_name: str = "sahayak_agent"
    context: Dict[str, Any] = {}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model": config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else "cloud",
        "server": "local" if config.USE_LOCAL_MODEL else "cloud"
    }

@app.post("/chat")
async def chat_completion(request: ChatRequest):
    """OpenAI-compatible chat completion endpoint"""
    if not local_client:
        raise HTTPException(status_code=400, detail="Local model not configured")
    
    try:
        # Convert messages to a prompt
        messages = [msg.dict() for msg in request.messages]
        response = local_client.chat_completion(
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return {
            "id": "local-completion",
            "object": "chat.completion",
            "model": config.LOCAL_MODEL_NAME,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response
                }
            }]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/agent")
async def run_agent(request: AgentRequest):
    """Run a specific agent with local model"""
    if not local_client:
        raise HTTPException(status_code=400, detail="Local model not configured")
    
    try:
        # Route to different agents based on agent_name
        if request.agent_name == "content_gen_agent":
            prompt = f"""Task: Create educational content for rural Indian school children.

Request: {request.message}

Requirements:
- Appropriate for multi-grade classrooms
- Simple, clear language
- Culturally relevant to rural India
- Practical for teachers with limited resources

Content:"""
        
        elif request.agent_name == "story_agent":
            prompt = f"""Task: Write a short educational story for children.

Topic: {request.message}

Requirements:
- Age-appropriate for young students
- Set in rural Indian context
- Include a learning element
- Complete story with beginning, middle, and end

Story:"""
        
        elif request.agent_name == "worksheet_agent":
            prompt = f"""Task: Create a practice worksheet for students.

Subject: {request.message}

Format:
- Clear title
- Simple instructions
- 3-5 practice problems
- Answer spaces

Worksheet:

Title: _______________

Instructions: _______________

Problems:
1."""
        
        elif request.agent_name == "visual_aid_agent":
            prompt = f"""Task: Create step-by-step drawing instructions for teachers.

Topic: {request.message}

Provide detailed instructions for blackboard/whiteboard drawing:
- Materials needed
- Step-by-step drawing process
- Labels and annotations to add

Instructions:"""
        
        else:  # root_agent
            prompt = f"""You are Sahayak AI, helping rural Indian teachers.

Teacher's request: {request.message}

Provide practical educational advice that works in multi-grade classrooms with limited resources.

Advice:"""
        
        response = local_client.generate_text(
            prompt=prompt,
            max_tokens=512,
            temperature=0.7
        )
        
        return {
            "agent": request.agent_name,
            "message": request.message,
            "response": response,
            "model": config.LOCAL_MODEL_NAME,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.get("/agents")
async def list_agents():
    """List available agents"""
    return {
        "agents": [
            {
                "name": "sahayak_agent",
                "description": "Main educational assistant",
                "model": config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else "cloud"
            },
            {
                "name": "content_gen_agent", 
                "description": "Educational content generator",
                "model": config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else "cloud"
            },
            {
                "name": "story_agent",
                "description": "Educational story creator",
                "model": config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else "cloud"
            },
            {
                "name": "worksheet_agent",
                "description": "Practice worksheet creator", 
                "model": config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else "cloud"
            },
            {
                "name": "visual_aid_agent",
                "description": "Visual aid instruction generator",
                "model": config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else "cloud"
            }
        ]
    }

if __name__ == "__main__":
    print("🚀 Starting Sahayak AI Local Development Server...")
    print(f"🔧 Model: {config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else 'Cloud Model'}")
    print(f"🌐 URL: {config.LOCAL_MODEL_URL if config.USE_LOCAL_MODEL else 'Cloud'}")
    print(f"📚 Server will run at: http://localhost:8000")
    print(f"📖 API Docs: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
