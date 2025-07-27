#!/usr/bin/env python3
"""
Simplified FastAPI server for Sahayak AI demonstration.
This version works without Google ADK dependencies for demo purposes.
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
import random
import time

# Load environment variables
load_dotenv()

# Import config for local model settings
from sahayakai import config

app = FastAPI(
    title="Sahayak AI Agent Server (Demo)",
    description="REST API for the Sahayak AI Educational Assistant - Demo Version",
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

# Mock agent configuration - use local model if configured
model_name = config.LOCAL_MODEL_NAME if config.USE_LOCAL_MODEL else "gemini-2.0-flash-exp"
MOCK_AGENT = {
    "name": "sahayak_agent",
    "model": model_name,
    "description": f"Sahayak AI Educational Assistant ({'Local' if config.USE_LOCAL_MODEL else 'Cloud'} Mode)"
}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        agent_name=MOCK_AGENT["name"],
        model=MOCK_AGENT["model"]
    )

async def generate_educational_response(message: str) -> str:
    """
    Generate educational responses based on the message content.
    This simulates the multi-agent system behavior.
    """
    message_lower = message.lower()
    
    # Simulate processing time
    await asyncio.sleep(random.uniform(1, 3))
    
    if any(word in message_lower for word in ["lesson", "plan", "teach", "class"]):
        return f"""
## 📚 Lesson Plan Generated

**Topic Analysis**: Based on your request "{message}", I've created a comprehensive lesson plan.

### 🎯 Learning Objectives
- Students will understand the core concepts
- Hands-on activities will reinforce learning
- Assessment will measure comprehension

### 📋 Lesson Structure
1. **Introduction** (10 minutes)
   - Warm-up activity
   - Prior knowledge assessment

2. **Main Content** (25 minutes)
   - Concept explanation with examples
   - Interactive demonstrations
   - Student participation activities

3. **Practice** (15 minutes)
   - Guided practice exercises
   - Peer collaboration

4. **Conclusion** (10 minutes)
   - Summary and review
   - Questions and clarifications

### 🎨 Visual Aids
- Diagrams and charts
- Real-world examples
- Interactive elements

### 📝 Assessment
- Quick formative assessment
- Exit ticket questions
- Homework assignment

**🤖 Agents Involved**: Content Generation Agent, Visual Aid Agent, Worksheet Agent

**✅ Status**: Ready for classroom implementation
"""
    
    elif any(word in message_lower for word in ["image", "visual", "picture", "diagram"]):
        return f"""
## 🎨 Visual Aid Generation

**Request**: {message}

### 📸 Visual Content Created
- Educational diagrams tailored to the topic
- Age-appropriate illustrations
- Culturally relevant imagery for Indian classrooms

### 🎯 Visual Elements
- **Main Concept Diagram**: Clear, labeled illustrations
- **Step-by-step Visuals**: Process breakdown
- **Interactive Elements**: Engaging visual components
- **Cultural Context**: Relevant to rural Indian settings

### 📊 Technical Details
- High-resolution images suitable for printing
- Mobile-friendly formats
- Accessible design with clear text

**🖼️ Generated Using**: Imagen 3 model via Visual Aid Agent

**✅ Status**: Visual aids ready for download and classroom use

**📱 Usage**: Perfect for digital displays or printed handouts
"""
    
    elif any(word in message_lower for word in ["worksheet", "exercise", "practice", "assignment"]):
        return f"""
## 📝 Worksheet Generated

**Subject**: Based on your request - {message}

### 🎯 Learning Goals
- Reinforce key concepts through practice
- Provide structured learning activities
- Enable self-assessment opportunities

### 📋 Worksheet Sections

#### Section A: Multiple Choice (5 questions)
- Fundamental concept understanding
- Quick knowledge checks

#### Section B: Short Answers (3 questions)
- Application of concepts
- Critical thinking exercises

#### Section C: Problem Solving (2 questions)
- Real-world applications
- Step-by-step solutions required

#### Section D: Creative Activity (1 task)
- Open-ended exploration
- Encourages creativity and deeper understanding

### 🏆 Assessment Rubric
- **Excellent** (4 points): Complete understanding and application
- **Good** (3 points): Good grasp with minor gaps
- **Satisfactory** (2 points): Basic understanding
- **Needs Improvement** (1 point): Requires additional support

**🤖 Created by**: Worksheet Agent with pedagogical optimization

**✅ Ready for**: Printing and classroom distribution
"""
    
    elif any(word in message_lower for word in ["story", "tale", "narrative"]):
        return f"""
## 📖 Educational Story Generated

**Theme**: Inspired by your request - {message}

### 🌟 Story: "The Curious Adventures of Learning"

Once upon a time, in a small village in India, there lived a young student who was curious about the world around them. This story will teach important concepts through engaging narrative...

### 📚 Story Elements
- **Characters**: Relatable protagonists for students
- **Setting**: Rural Indian context for cultural relevance
- **Plot**: Educational journey with clear learning moments
- **Moral**: Reinforces the lesson objectives

### 🎯 Educational Value
- Culturally appropriate content
- Age-appropriate language and concepts
- Interactive discussion points
- Connection to curriculum goals

### 💡 Teaching Tips
- Read aloud with expression
- Pause for student predictions
- Discuss key learning moments
- Connect to students' experiences

**📝 Story Agent**: Specialized in culturally relevant educational narratives

**✅ Status**: Ready for classroom storytelling

**🎭 Extension Activities**: Role-playing, illustration, retelling
"""
    
    elif any(word in message_lower for word in ["translate", "hindi", "telugu", "tamil", "bengali", "marathi", "gujarati"]):
        return f"""
## 🌍 Multilingual Content Generated

**Original Request**: {message}

### 🗣️ Language Support
Content has been adapted for multilingual classroom needs:

#### 📝 Available Languages
- **English**: Primary content language
- **Hindi**: हिंदी में अनुवादित सामग्री
- **Telugu**: తెలుగులో అనువాదం
- **Tamil**: தமிழில் மொழிபெயர்ப்பு
- **Bengali**: বাংলায় অনুবাদ
- **Marathi**: मराठीत भाषांतर
- **Gujarati**: ગુજરાતીમાં અનુવાદ

### 🎯 Cultural Adaptation
- Locally relevant examples
- Culturally appropriate contexts
- Regional learning preferences
- Community-specific references

### 📚 Implementation Guide
- Start with familiar language
- Gradually introduce English terms
- Use code-switching effectively
- Encourage peer translation

**🌐 Translation Agent**: Specialized in Indian educational contexts

**✅ Status**: Multi-language content ready for diverse classrooms
"""
    
    else:
        return f"""
## 🤖 Sahayak AI Response

**Your Request**: {message}

### 🎓 Educational Assistant Ready
Thank you for reaching out to Sahayak AI! I'm designed to help teachers in rural, multi-grade classrooms across India.

### 🚀 My Capabilities
- **Lesson Planning**: Comprehensive educational content
- **Visual Aids**: Images, diagrams, and illustrations
- **Worksheets**: Practice exercises and assessments
- **Stories**: Educational narratives and tales
- **Translations**: Multi-language support
- **Cultural Adaptation**: Content suitable for Indian classrooms

### 💡 How to Get Started
Try asking me to:
- "Create a lesson plan on [topic] for grade [X] students"
- "Generate visual aids for teaching [subject]"
- "Make a worksheet about [concept]"
- "Tell a story about [topic] for young learners"
- "Translate this content to [language]"

### 🎯 Specialized for Rural Education
- Multi-grade classroom support
- Resource-efficient solutions
- Culturally relevant content
- Offline-capable design

**🤝 Ready to help**: Ask me anything about educational content creation!

**🌟 Status**: All agent systems operational and ready to assist
"""

async def invoke_agent(message: str, conversation_id: str) -> str:
    """
    Invoke the educational agent system.
    """
    try:
        response = await generate_educational_response(message)
        return response
    except Exception as e:
        return f"I apologize, but I encountered an error while processing your request: {str(e)}. Please try again or rephrase your question."

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
            await asyncio.sleep(0.05)  # Small delay for streaming effect
        
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
        "agent_name": MOCK_AGENT["name"],
        "model": MOCK_AGENT["model"],
        "description": "Sahayak AI - Multi-agent system for rural classroom education (Demo Mode)",
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
            "Translation Agent"
        ],
        "supported_languages": [
            "English",
            "Hindi", 
            "Telugu",
            "Tamil",
            "Bengali",
            "Marathi",
            "Gujarati"
        ],
        "note": "This is a demo version. Full ADK integration available in production."
    }

@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "name": "Sahayak AI Agent Server (Demo)",
        "status": "running",
        "agent": MOCK_AGENT["name"],
        "description": "Educational assistant for rural multi-grade classrooms - Demo Mode",
        "note": "This is a demonstration version with simulated agent responses",
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
    
    print("🎓 Starting Sahayak AI Educational Assistant (Demo Mode)")
    print("=" * 60)
    print(f"🚀 Server: http://{host}:{port}")
    print(f"🤖 Agent: {MOCK_AGENT['name']}")
    print(f"🧠 Model: {MOCK_AGENT['model']} (Simulated)")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print("=" * 60)
    print("🌟 Ready to assist with educational content generation!")
    print("💡 This is a demo version - try asking for lesson plans, worksheets, or visual aids")
    print("")
    
    uvicorn.run(
        "demo_server:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
