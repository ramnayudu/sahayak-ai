from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="AI Sahayak API", description="AI-Powered Multi-Grade Classroom Assistant", version="1.0.0")

# Enable CORS for all origins (you can restrict this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files from frontend directory
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def root():
    return {"message": "AI Sahayak Backend is running!", "status": "online", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Sahayak Backend"}

@app.get("/api/")
async def api_root():
    return {"message": "AI Sahayak API is running!", "status": "online", "version": "1.0.0"}

@app.get("/api/health")
async def api_health_check():
    return {"status": "healthy", "service": "AI Sahayak API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
