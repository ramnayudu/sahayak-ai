# 🎓 Sahayak AI Streamlit App

A beautiful Streamlit interface for the Sahayak AI educational assistant, featuring the Google ADK-powered multi-agent system.

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
# Run the start script (recommended)
./start_streamlit.sh
```

### Option 2: Manual Setup

#### 1. Install Dependencies
```bash
# Install Streamlit dependencies
pip install -r requirements.txt

# Install backend dependencies
cd agentic-backend
poetry install  # or pip install fastapi uvicorn python-dotenv
cd ..
```

#### 2. Start Backend Server
```bash
cd agentic-backend
python server.py
```

#### 3. Start Streamlit App
```bash
streamlit run streamlit_app.py
```

## 📱 Access Points

- **Streamlit App**: http://localhost:8501
- **Backend API**: http://localhost:8000  
- **API Documentation**: http://localhost:8000/docs

## 🎯 Features

### 🤖 AI Capabilities
- **Lesson Plan Generation**: Create comprehensive lesson plans for any subject and grade
- **Visual Aid Creation**: Generate educational images and diagrams
- **Worksheet Development**: Create practice exercises and assessments
- **Story Generation**: Educational stories tailored to age groups
- **Multi-language Support**: Content in English, Hindi, Telugu, Tamil, and more

### 💬 Chat Interface
- **Real-time Chat**: Interactive conversation with the AI agent
- **Conversation History**: Track and review previous interactions
- **Sample Prompts**: Quick access to common educational requests
- **Streaming Responses**: Real-time response generation

### 🔧 System Features
- **Health Monitoring**: Real-time backend connection status
- **Agent Information**: Detailed view of agent capabilities and sub-agents
- **API Integration**: Full REST API integration with error handling
- **Responsive Design**: Works on desktop and mobile devices

## 🎨 User Interface

### Main Dashboard
- **Chat Interface**: Primary interaction area with the AI agent
- **Status Panel**: Real-time system health and connection status
- **Agent Details**: Information about loaded agents and capabilities
- **Quick Actions**: Common tasks and sample prompts

### Sample Prompts
Try these example prompts to get started:

1. "Create a lesson plan on fractions for grade 4 students"
2. "Generate visual aids for teaching photosynthesis"
3. "Create a worksheet on basic multiplication"
4. "Tell a story about water cycle for young children"
5. "Generate class activities for teaching Hindi alphabets"

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: FastAPI server exposing the ADK agent
- **AI System**: Google ADK multi-agent system
- **Communication**: REST API with JSON payloads

### API Endpoints
- `GET /health` - Check system health
- `POST /chat` - Send message to agent
- `POST /chat/stream` - Stream responses
- `GET /conversations` - List conversations
- `GET /agent-info` - Agent capabilities

### Error Handling
- Connection monitoring with automatic retry
- Graceful degradation when backend is unavailable
- User-friendly error messages
- Fallback demo content

## 🎓 Educational Context

This application is designed specifically for:

- **Rural Classrooms**: Supporting teachers in resource-limited environments
- **Multi-grade Teaching**: Content adapted for mixed-age classrooms
- **Indian Education**: Culturally relevant content and multiple languages
- **Teacher Empowerment**: Easy-to-use tools for lesson preparation

## 🔍 Troubleshooting

### Backend Not Connecting
1. Ensure the backend server is running on port 8000
2. Check if all dependencies are installed
3. Verify the ADK agent configuration
4. Check the terminal for error messages

### Streamlit Issues
1. Refresh the browser page
2. Clear browser cache
3. Restart the Streamlit server
4. Check Python package versions

### Agent Errors
1. Verify Google Cloud credentials are set up
2. Check internet connection for online models
3. Ensure ADK dependencies are properly installed
4. Review agent configuration files

## 📚 Documentation

- [Project Setup Guide](SETUP.md)
- [Agent Framework Documentation](docs/agent_framework.md)
- [Deployment Guide](docs/deployment.md)
- [API Documentation](http://localhost:8000/docs) (when server is running)

## 🤝 Contributing

This Streamlit app is part of the larger Sahayak AI project. For contribution guidelines, please see the main project documentation.

## 📄 License

This project is part of Sahayak AI and follows the same licensing terms.
