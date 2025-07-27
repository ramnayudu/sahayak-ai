#!/usr/bin/env python3
"""
Simple test server for Sahayak AI demo
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Sahayak AI Test")

@app.get("/")
def root():
    return {"message": "Sahayak AI Test Server Running!"}

@app.get("/health")
def health():
    return {"status": "healthy", "agent_name": "test_agent", "model": "test_model"}

@app.post("/chat")
def chat(request: dict):
    message = request.get("message", "")
    return {
        "response": f"Echo: {message}",
        "conversation_id": "test_conv",
        "status": "success"
    }

if __name__ == "__main__":
    print("Starting simple test server...")
    uvicorn.run("simple_server:app", host="0.0.0.0", port=8000, reload=True)
