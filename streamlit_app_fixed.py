import streamlit as st
import requests
import json
import time
from typing import Dict, List, Optional
import uuid

# ADK Chat Interface Class
class ADKChat:
    def __init__(self):
        self.adk_base_url = "http://localhost:8000"
    
    def format_adk_response(self, response):
        """Format the ADK response into readable text"""
        # Handle different response structures
        if isinstance(response, dict):
            if 'response' in response:
                response_data = response['response']
            else:
                response_data = response
        else:
            return str(response)
        
        # Try to extract text from candidates
        if 'candidates' in response_data:
            response_list = response_data['candidates']
        elif isinstance(response_data, list):
            response_list = response_data
        else:
            response_list = [response_data]
        
        # If no text response found, look for function responses with results
        final_result = ""
        for item in response_list:
            if 'content' in item and 'parts' in item['content']:
                for part in item['content']['parts']:
                    if 'functionResponse' in part:
                        func_resp = part['functionResponse']
                        if 'response' in func_resp and 'result' in func_resp['response']:
                            result = func_resp['response']['result']
                            if isinstance(result, str) and result.strip():
                                final_result = result
        
        if final_result:
            return self.clean_response_text(final_result)
        
        # Fallback - return a clean message
        return "Response received from agent (no readable content found)"
    
    def clean_response_text(self, text):
        """Clean up the response text by removing markdown artifacts while keeping explanations"""
        if not isinstance(text, str):
            return str(text)
        
        # Debug: Show original text
        print(f"DEBUG: Original text: {repr(text)}")
        
        # Remove common markdown wrappers
        text = text.strip()
        
        # Remove **Result:** prefix
        if text.startswith('**Result:**'):
            text = text.replace('**Result:**', '').strip()
        
        # Remove markdown code blocks (``` at start and end)
        if text.startswith('```') and text.endswith('```'):
            text = text[3:-3].strip()
        
        # Remove any remaining ``` at the beginning or end (multiple passes)
        while text.startswith('```'):
            text = text[3:].strip()
        while text.endswith('```'):
            text = text[:-3].strip()
        
        # Process line by line but keep everything including explanations
        lines = text.split('\n')
        final_lines = []
        
        for line in lines:
            # Keep all lines - don't filter out explanations anymore
            final_lines.append(line)
        
        # Join back and clean up extra whitespace
        cleaned_text = '\n'.join(final_lines).strip()
        
        # Remove multiple consecutive newlines
        import re
        cleaned_text = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_text)
        
        # Final cleanup for any remaining ``` scattered in the text
        cleaned_text = re.sub(r'```\s*$', '', cleaned_text).strip()
        cleaned_text = re.sub(r'```', '', cleaned_text).strip()
        
        # Debug: Show cleaned text
        print(f"DEBUG: Cleaned text: {repr(cleaned_text)}")
        
        return cleaned_text
    
    def create_session(self):
        """Create a new session with the ADK agent"""
        try:
            # First, check if we have a session
            if not hasattr(st.session_state, 'adk_session_id'):
                # Create a new session using ADK session endpoint
                payload = {"stateDelta": {}}
                response = requests.post(
                    f"{self.adk_base_url}/apps/sahayakai/users/streamlit_user/sessions",
                    json=payload,
                    timeout=10
                )
                if response.status_code == 200:
                    session_info = response.json()
                    # The session ID is in the 'id' field
                    st.session_state.adk_session_id = session_info.get('id')
                    return True
                else:
                    st.error(f"Failed to create session: {response.status_code} - {response.text}")
                    return False
            return True
        except Exception as e:
            st.error(f"Error creating session: {str(e)}")
            return False
    
    def send_message(self, message):
        """Send a message to the ADK agent and return the response"""
        try:
            # Ensure we have a session
            if not self.create_session():
                return "Failed to create session with ADK agent."
            
            payload = {
                "appName": "sahayakai",
                "userId": "streamlit_user",
                "sessionId": st.session_state.adk_session_id,
                "newMessage": {
                    "parts": [{"text": message}],
                    "role": "user"
                },
                "streaming": False
            }
            
            response = requests.post(f"{self.adk_base_url}/run", json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return self.format_adk_response(result)
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error sending message: {str(e)}"

# Page configuration
st.set_page_config(
    page_title="Sahayak AI - Educational Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        background-color: #f8f9fa;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .assistant-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    
    .sidebar-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background-color: #28a745;
    }
    
    .status-offline {
        background-color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Initialize ADK Chat
if 'adk_chat' not in st.session_state:
    st.session_state.adk_chat = ADKChat()

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Helper functions
def check_api_health() -> Dict:
    """Check if the ADK API is accessible"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            return {"status": "online", "message": "ADK Agent is running"}
        else:
            return {"status": "error", "message": f"ADK returned status {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"status": "offline", "message": "Cannot connect to ADK Agent (http://localhost:8000)"}
    except requests.exceptions.Timeout:
        return {"status": "timeout", "message": "ADK Agent is not responding"}
    except Exception as e:
        return {"status": "error", "message": f"Error checking ADK status: {str(e)}"}

def display_message(role, content):
    """Display a chat message with proper styling"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>Sahayak AI:</strong><br>
            {content.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)

def clear_chat():
    """Clear the chat history"""
    st.session_state.messages = []
    # Also clear the session to start fresh
    if hasattr(st.session_state, 'adk_session_id'):
        del st.session_state.adk_session_id

def get_agent_info() -> Optional[Dict]:
    """Get information about the available agents"""
    try:
        response = requests.get("http://localhost:8000/apps", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def export_conversation():
    """Export the conversation as JSON"""
    if st.session_state.messages:
        return json.dumps(st.session_state.messages, indent=2)
    return "No conversation to export"

def get_conversation_stats():
    """Get statistics about the current conversation"""
    if not st.session_state.messages:
        return "No messages yet"
    
    user_messages = sum(1 for msg in st.session_state.messages if msg["role"] == "user")
    assistant_messages = sum(1 for msg in st.session_state.messages if msg["role"] == "assistant")
    
    return f"Messages: {len(st.session_state.messages)} (You: {user_messages}, AI: {assistant_messages})"

def get_conversation_history(conversation_id: str) -> Optional[List[Dict]]:
    """Get conversation history from ADK (if available)"""
    try:
        response = requests.get(f"http://localhost:8000/conversations/{conversation_id}", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="main-header">
        <h2>🎓 Sahayak AI</h2>
        <p>Your Educational Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status check
    st.subheader("🔌 Connection Status")
    api_status = check_api_health()
    
    if api_status["status"] == "online":
        st.markdown(f"""
        <div class="sidebar-info">
            <span class="status-indicator status-online"></span>
            <strong>Connected</strong><br>
            {api_status["message"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="sidebar-info" style="border-left-color: #dc3545;">
            <span class="status-indicator status-offline"></span>
            <strong>Disconnected</strong><br>
            {api_status["message"]}
        </div>
        """, unsafe_allow_html=True)
        
        st.warning("⚠️ Please make sure the ADK Agent is running on http://localhost:8000")
    
    # Agent Information
    st.subheader("🤖 Agent Info")
    agent_info = get_agent_info()
    if agent_info:
        st.json(agent_info)
    else:
        st.info("No agent information available")
    
    # Conversation Stats
    st.subheader("📊 Conversation Stats")
    st.info(get_conversation_stats())
    
    # Controls
    st.subheader("🛠️ Controls")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat()
            st.rerun()
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Export conversation
    if st.session_state.messages:
        if st.button("📥 Export Chat", use_container_width=True):
            exported_data = export_conversation()
            st.download_button(
                label="💾 Download JSON",
                data=exported_data,
                file_name=f"sahayak_conversation_{int(time.time())}.json",
                mime="application/json",
                use_container_width=True
            )

# Main content area
st.markdown("""
<div class="main-header">
    <h1>🎓 Sahayak AI - Educational Assistant</h1>
    <p>Powered by Google's Agent Development Kit (ADK)</p>
</div>
""", unsafe_allow_html=True)

# Features overview
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>📚 Content Generation</h4>
        <p>Create educational materials, lesson plans, and worksheets</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>📖 Storytelling</h4>
        <p>Generate engaging educational stories and narratives</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>🎨 Visual Aids</h4>
        <p>Create visual learning materials and educational graphics</p>
    </div>
    """, unsafe_allow_html=True)

# Chat interface
st.subheader("💬 Chat with Sahayak AI")

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        display_message(message["role"], message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about education, lesson planning, or learning materials..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with chat_container:
        display_message("user", prompt)
    
    # Show typing indicator
    with st.spinner("Sahayak AI is thinking..."):
        # Get response from ADK
        response = st.session_state.adk_chat.send_message(prompt)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display assistant response
    with chat_container:
        display_message("assistant", response)
    
    # Rerun to update the display
    st.rerun()

# Quick action buttons
st.subheader("🚀 Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📝 Create Lesson Plan", use_container_width=True):
        quick_prompt = "Create a comprehensive lesson plan for 5th grade students about the solar system"
        st.session_state.messages.append({"role": "user", "content": quick_prompt})
        with st.spinner("Creating lesson plan..."):
            response = st.session_state.adk_chat.send_message(quick_prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col2:
    if st.button("📊 Generate Worksheet", use_container_width=True):
        quick_prompt = "Create a worksheet for 3rd grade students about basic multiplication"
        st.session_state.messages.append({"role": "user", "content": quick_prompt})
        with st.spinner("Generating worksheet..."):
            response = st.session_state.adk_chat.send_message(quick_prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col3:
    if st.button("📚 Create Story", use_container_width=True):
        quick_prompt = "Write an educational story for kids about the importance of recycling"
        st.session_state.messages.append({"role": "user", "content": quick_prompt})
        with st.spinner("Writing story..."):
            response = st.session_state.adk_chat.send_message(quick_prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col4:
    if st.button("🎨 Visual Learning Aid", use_container_width=True):
        quick_prompt = "Create a visual learning aid to explain the water cycle to elementary students"
        st.session_state.messages.append({"role": "user", "content": quick_prompt})
        with st.spinner("Creating visual aid..."):
            response = st.session_state.adk_chat.send_message(quick_prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🎓 Sahayak AI - Empowering Education with AI | Built with Streamlit & Google ADK</p>
    <p><small>Version 1.0 | Educational Assistant Platform</small></p>
</div>
""", unsafe_allow_html=True)
