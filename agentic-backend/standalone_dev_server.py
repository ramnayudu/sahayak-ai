#!/usr/bin/env python3
"""
Standalone Local Development Server for Sahayak AI
This server allows testing with Transformer Lab without ADK dependencies
"""

import os
import requests
import json
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

# Configuration
USE_LOCAL_MODEL = os.getenv('USE_LOCAL_MODEL', 'false').lower() == 'true'
LOCAL_MODEL_URL = os.getenv('LOCAL_MODEL_URL', 'http://localhost:21002')
LOCAL_MODEL_NAME = os.getenv('LOCAL_MODEL_NAME', 'gemma-3-1b-pt')

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

class TransformerLabClient:
    """Simple client for Transformer Lab"""
    
    def __init__(self):
        self.base_url = LOCAL_MODEL_URL
        self.timeout = 30.0
    
    def generate_text(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        """Generate text using Transformer Lab"""
        
        url = f"{self.base_url.rstrip('/')}/worker_generate"
        headers = {"Content-Type": "application/json"}
        
        request_data = {
            "prompt": prompt,
            "max_new_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "repetition_penalty": 1.2,
            "do_sample": True,
        }
        
        try:
            response = requests.post(url, json=request_data, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            
            generated_text = result.get("text", "")
            
            if generated_text:
                # Clean up the response
                if generated_text.startswith(prompt):
                    generated_text = generated_text[len(prompt):].strip()
                
                # Remove artifacts and clean up repetitive content
                lines = generated_text.split('\n')
                unique_lines = []
                seen_lines = set()
                
                for line in lines:
                    line = line.strip()
                    if (line and 
                        line not in seen_lines and 
                        len(line) > 5 and
                        not line.startswith('[User') and 
                        not line.startswith('User ')):
                        
                        unique_lines.append(line)
                        seen_lines.add(line)
                        
                        if len(unique_lines) >= 3:
                            break
                
                if unique_lines:
                    result = ' '.join(unique_lines)
                    # Ensure complete sentences
                    sentences = result.split('. ')
                    if len(sentences) > 1 and not sentences[-1].endswith(('.', '!', '?')):
                        result = '. '.join(sentences[:-1]) + '.'
                    return result.strip()
                else:
                    return generated_text.strip()
            
            return "No response generated"
            
        except Exception as e:
            return f"Error: Could not generate response - {str(e)}"

# Initialize client
local_client = TransformerLabClient() if USE_LOCAL_MODEL else None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
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
        "model": LOCAL_MODEL_NAME if USE_LOCAL_MODEL else "cloud",
        "server": "local-standalone" if USE_LOCAL_MODEL else "cloud"
    }

@app.post("/chat")
async def chat_completion(request: ChatRequest):
    """OpenAI-compatible chat completion endpoint"""
    if not local_client:
        raise HTTPException(status_code=400, detail="Local model not configured")
    
    try:
        # Convert messages to a prompt
        prompt_parts = []
        for msg in request.messages:
            if msg.role == "system":
                prompt_parts.append(f"System: {msg.content}")
            elif msg.role == "user":
                prompt_parts.append(f"User: {msg.content}")
            elif msg.role == "assistant":
                prompt_parts.append(f"Assistant: {msg.content}")
        
        prompt = "\n".join(prompt_parts)
        if not prompt.endswith("Assistant:"):
            prompt += "\nAssistant:"
        
        response = local_client.generate_text(
            prompt=prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return {
            "id": "local-completion",
            "object": "chat.completion",
            "model": LOCAL_MODEL_NAME,
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
        # Create agent-specific prompts
        if request.agent_name == "content_gen_agent":
            prompt = f"""Task: Create educational content for rural Indian school children.

Request: {request.message}

Create content that is:
- Appropriate for multi-grade classrooms
- Simple, clear language
- Culturally relevant to rural India
- Practical for teachers with limited resources

Content:"""
        
        elif request.agent_name == "story_agent":
            prompt = f"""Task: Write a short educational story for children.

Topic: {request.message}

Create a story that is:
- Age-appropriate for young students
- Set in rural Indian context
- Include a learning element
- Complete with beginning, middle, and end

Story:"""
        
        elif request.agent_name == "worksheet_agent":
            prompt = f"""Task: Create a practice worksheet for students.

Subject: {request.message}

Create a worksheet with:
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
- Materials needed (chalk, markers, etc.)
- Step-by-step drawing process
- Labels and annotations to add
- Interactive elements for students

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
            "model": LOCAL_MODEL_NAME,
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
                "model": LOCAL_MODEL_NAME if USE_LOCAL_MODEL else "cloud"
            },
            {
                "name": "content_gen_agent", 
                "description": "Educational content generator",
                "model": LOCAL_MODEL_NAME if USE_LOCAL_MODEL else "cloud"
            },
            {
                "name": "story_agent",
                "description": "Educational story creator",
                "model": LOCAL_MODEL_NAME if USE_LOCAL_MODEL else "cloud"
            },
            {
                "name": "worksheet_agent",
                "description": "Practice worksheet creator", 
                "model": LOCAL_MODEL_NAME if USE_LOCAL_MODEL else "cloud"
            },
            {
                "name": "visual_aid_agent",
                "description": "Visual aid instruction generator",
                "model": LOCAL_MODEL_NAME if USE_LOCAL_MODEL else "cloud"
            }
        ]
    }

if __name__ == "__main__":
    print("🚀 Starting Sahayak AI Standalone Local Development Server...")
    print(f"🔧 Model: {LOCAL_MODEL_NAME if USE_LOCAL_MODEL else 'Cloud Model'}")
    print(f"🌐 URL: {LOCAL_MODEL_URL if USE_LOCAL_MODEL else 'Cloud'}")
    print(f"📚 Server will run at: http://localhost:8080")
    print(f"📖 API Docs: http://localhost:8080/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8080)
