import streamlit as st
import requests
import json
import time
from typing import Dict, List, Optional
import uuid
import os
from PIL import Image
import base64
import io

# ADK Chat Interface Class
class ADKChat:
    def __init__(self):
        self.adk_base_url = "http://localhost:8000"
    
    def format_adk_response(self, response):
        """Format the ADK response into readable text and handle images"""
        print(f"DEBUG: Raw response type: {type(response)}")
        print(f"DEBUG: Raw response: {str(response)[:500]}...")
        
        # Log the full structure for debugging
        try:
            if isinstance(response, (dict, list)):
                print(f"DEBUG: Full response structure: {json.dumps(response, indent=2)[:1000]}...")
        except:
            print("DEBUG: Could not serialize full response")
        
        # Handle different response structures
        if isinstance(response, dict):
            if 'response' in response:
                response_data = response['response']
            else:
                response_data = response
        elif isinstance(response, list):
            # Response is already a list
            response_data = response
        else:
            return str(response)
        
        # Try to extract text from candidates
        if isinstance(response_data, dict) and 'candidates' in response_data:
            response_list = response_data['candidates']
        elif isinstance(response_data, list):
            response_list = response_data
        else:
            response_list = [response_data]
        
        # Look for function responses with results and images
        final_result = ""
        images_data = []
        print(f"DEBUG: Processing {len(response_list)} response items")
        
        for i, item in enumerate(response_list):
            print(f"DEBUG: Item {i}: {item.keys() if isinstance(item, dict) else type(item)}")
            if 'content' in item and 'parts' in item['content']:
                print(f"DEBUG: Item {i} has content with {len(item['content']['parts'])} parts")
                for j, part in enumerate(item['content']['parts']):
                    print(f"DEBUG: Part {j}: {part.keys() if isinstance(part, dict) else type(part)}")
                    
                    # Check for text content
                    if 'text' in part:
                        text_content = part['text']
                        print(f"DEBUG: Found text content: {text_content[:200]}...")
                        if isinstance(text_content, str) and text_content.strip():
                            final_result = text_content
                    
                    # Check for inline image data
                    elif 'inlineData' in part:
                        inline_data = part['inlineData']
                        print(f"DEBUG: Found inline data: {inline_data.keys()}")
                        if 'mimeType' in inline_data and inline_data['mimeType'].startswith('image/'):
                            images_data.append(inline_data)
                            print(f"DEBUG: Found image data with mime type: {inline_data['mimeType']}")
                    
                    # Check for function responses
                    elif 'functionResponse' in part:
                        func_resp = part['functionResponse']
                        print(f"DEBUG: Found functionResponse: {func_resp.keys()}")
                        
                        # Log the full function response structure
                        try:
                            print(f"DEBUG: Full function response: {json.dumps(func_resp, indent=2)[:500]}...")
                        except:
                            print("DEBUG: Could not serialize function response")
                        
                        if 'response' in func_resp and 'result' in func_resp['response']:
                            result = func_resp['response']['result']
                            print(f"DEBUG: Found result: {result[:200]}...")
                            if isinstance(result, str) and result.strip():
                                final_result = result
                        
                        # Check if function response contains image data in various formats
                        if 'response' in func_resp:
                            func_response = func_resp['response']
                            # Check for different possible image storage formats
                            for key in ['images', 'image_data', 'generated_images', 'attachments']:
                                if key in func_response:
                                    func_images = func_response[key]
                                    print(f"DEBUG: Found {len(func_images) if isinstance(func_images, list) else 1} images in function response under key '{key}'")
                                    if isinstance(func_images, list):
                                        images_data.extend(func_images)
                                    else:
                                        images_data.append(func_images)
        
        # Clean the text result
        if final_result:
            cleaned_text = self.clean_response_text(final_result)
        else:
            cleaned_text = "Response received from agent (no readable content found)"
        
        # Display images if found in agent memory
        if images_data:
            print(f"DEBUG: Attempting to display {len(images_data)} images from agent memory")
            for i, image_data in enumerate(images_data):
                try:
                    print(f"DEBUG: Processing image {i+1}, type: {type(image_data)}, keys: {image_data.keys() if isinstance(image_data, dict) else 'N/A'}")
                    
                    if isinstance(image_data, dict) and 'data' in image_data:
                        # Handle base64 encoded image data
                        image_bytes = base64.b64decode(image_data['data'])
                        image = Image.open(io.BytesIO(image_bytes))
                        st.image(image, caption=f"Generated Image {i+1}", use_column_width=True)
                        print(f"DEBUG: Successfully displayed image {i+1} from agent memory")
                        cleaned_text += f"\n\n🖼️ **Generated Image {i+1}:** Displayed from agent memory"
                    elif isinstance(image_data, str) and image_data.startswith('data:image'):
                        # Handle data URL format
                        header, data = image_data.split(',', 1)
                        image_bytes = base64.b64decode(data)
                        image = Image.open(io.BytesIO(image_bytes))
                        st.image(image, caption=f"Generated Image {i+1}", use_column_width=True)
                        print(f"DEBUG: Successfully displayed data URL image {i+1}")
                        cleaned_text += f"\n\n🖼️ **Generated Image {i+1}:** Displayed from agent memory"
                    elif isinstance(image_data, str):
                        # Try to decode as base64 directly
                        try:
                            image_bytes = base64.b64decode(image_data)
                            image = Image.open(io.BytesIO(image_bytes))
                            st.image(image, caption=f"Generated Image {i+1}", use_column_width=True)
                            print(f"DEBUG: Successfully displayed base64 string image {i+1}")
                            cleaned_text += f"\n\n🖼️ **Generated Image {i+1}:** Displayed from agent memory"
                        except:
                            print(f"DEBUG: Could not decode image data as base64: {str(image_data)[:100]}...")
                            cleaned_text += f"\n\n🖼️ **Image Generated:** Image {i+1} (Could not decode)"
                    else:
                        print(f"DEBUG: Unknown image data format: {type(image_data)}, content: {str(image_data)[:100]}...")
                        cleaned_text += f"\n\n🖼️ **Image Generated:** Image {i+1} (Unknown format)"
                except Exception as e:
                    print(f"DEBUG: Error displaying image {i+1}: {e}")
                    cleaned_text += f"\n\n🖼️ **Image Generated:** Image {i+1} (Error displaying: {e})"
        else:
            print("DEBUG: No images found in agent response")
            # If this looks like a visual request, try to fetch artifacts
            if any(keyword in final_result.lower() for keyword in ['image', 'visual', 'diagram', 'picture', 'generated']):
                print("DEBUG: Visual content detected, attempting to fetch session artifacts")
                try:
                    self.fetch_session_images(cleaned_text)
                except:
                    pass
        
        return cleaned_text
    
    def fetch_session_images(self, current_text):
        """Try to fetch generated images from the session"""
        try:
            if hasattr(st.session_state, 'adk_session_id'):
                # Try different possible endpoints for artifacts
                endpoints_to_try = [
                    f"{self.adk_base_url}/apps/sahayakai/users/streamlit_user/sessions/{st.session_state.adk_session_id}/artifacts",
                    f"{self.adk_base_url}/apps/sahayakai/users/streamlit_user/sessions/{st.session_state.adk_session_id}/images",
                    f"{self.adk_base_url}/apps/sahayakai/users/streamlit_user/sessions/{st.session_state.adk_session_id}/files"
                ]
                
                for endpoint in endpoints_to_try:
                    try:
                        response = requests.get(endpoint, timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            print(f"DEBUG: Found data at {endpoint}: {type(data)} - {str(data)[:200]}...")
                            
                            # Process any image data found
                            if isinstance(data, list):
                                for item in data:
                                    if isinstance(item, str) and item.endswith('.png'):
                                        # Try to fetch the actual image file
                                        image_url = f"{endpoint}/{item}"
                                        print(f"DEBUG: Attempting to fetch image from: {image_url}")
                                        try:
                                            img_response = requests.get(image_url, timeout=10)
                                            if img_response.status_code == 200:
                                                # Check if it's image data
                                                if img_response.headers.get('content-type', '').startswith('image/'):
                                                    image = Image.open(io.BytesIO(img_response.content))
                                                    st.image(image, caption=f"Generated: {item}", use_column_width=True)
                                                    print(f"DEBUG: Successfully displayed image: {item}")
                                                else:
                                                    # Might be base64 encoded text
                                                    try:
                                                        img_data = img_response.text
                                                        if img_data.startswith('data:image'):
                                                            header, data = img_data.split(',', 1)
                                                            image_bytes = base64.b64decode(data)
                                                        else:
                                                            image_bytes = base64.b64decode(img_data)
                                                        image = Image.open(io.BytesIO(image_bytes))
                                                        st.image(image, caption=f"Generated: {item}", use_column_width=True)
                                                        print(f"DEBUG: Successfully displayed base64 image: {item}")
                                                    except Exception as e:
                                                        print(f"DEBUG: Could not decode image data: {e}")
                                        except requests.exceptions.RequestException as e:
                                            print(f"DEBUG: Could not fetch image {item}: {e}")
                                    elif isinstance(item, dict) and 'image' in str(item).lower():
                                        st.success(f"Found potential image data at {endpoint}")
                            elif isinstance(data, dict) and 'images' in data:
                                images = data['images']
                                st.success(f"Found {len(images)} images in session")
                                
                    except requests.exceptions.RequestException:
                        continue  # Try next endpoint
        except Exception as e:
            print(f"DEBUG: Error fetching session images: {e}")
    
    def clean_response_text(self, text):
        """Clean up the response text by removing markdown artifacts while keeping explanations"""
        if not isinstance(text, str):
            return str(text)
        
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
                "streaming": False,
                # Request image data to be included in response
                "includeImages": True,
                "includeArtifacts": True
            }
            
            response = requests.post(f"{self.adk_base_url}/run", json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                
                # Also check for artifacts in session after the run
                self.check_session_artifacts(result)
                
                return self.format_adk_response(result)
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error sending message: {str(e)}"
    
    def check_session_artifacts(self, run_result):
        """Check if there are any artifacts (like images) generated in the session"""
        try:
            if hasattr(st.session_state, 'adk_session_id'):
                session_id = st.session_state.adk_session_id
                
                # First try the artifacts endpoint directly
                artifacts_url = f"{self.adk_base_url}/apps/sahayakai/users/streamlit_user/sessions/{session_id}/artifacts"
                print(f"DEBUG: Checking artifacts at: {artifacts_url}")
                
                try:
                    artifacts_response = requests.get(artifacts_url, timeout=10)
                    if artifacts_response.status_code == 200:
                        artifacts = artifacts_response.json()
                        print(f"DEBUG: Artifacts response: {artifacts}")
                        
                        if isinstance(artifacts, list):
                            for artifact in artifacts:
                                if isinstance(artifact, str) and artifact.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                                    print(f"DEBUG: Found image artifact: {artifact}")
                                    success = self.fetch_artifact_image(session_id, artifact)
                                    if success:
                                        return True
                        elif isinstance(artifacts, dict):
                            for key, value in artifacts.items():
                                if key.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                                    print(f"DEBUG: Found image artifact key: {key}")
                                    success = self.fetch_artifact_image(session_id, key)
                                    if success:
                                        return True
                    else:
                        print(f"DEBUG: Artifacts endpoint failed: {artifacts_response.status_code}")
                except Exception as e:
                    print(f"DEBUG: Error with artifacts endpoint: {e}")
                
                # Also try to get session details to see if artifacts were created
                session_response = requests.get(
                    f"{self.adk_base_url}/apps/sahayakai/users/streamlit_user/sessions/{session_id}",
                    timeout=10
                )
                if session_response.status_code == 200:
                    session_data = session_response.json()
                    print(f"DEBUG: Session data keys: {session_data.keys() if isinstance(session_data, dict) else 'Not a dict'}")
                    
                    # Look for artifacts, images, or generated content
                    if 'artifacts' in session_data:
                        print(f"DEBUG: Found artifacts in session: {session_data['artifacts']}")
                    if 'images' in session_data:
                        print(f"DEBUG: Found images in session: {len(session_data['images'])}")
                    if 'state' in session_data:
                        state = session_data['state']
                        print(f"DEBUG: Session state keys: {state.keys() if isinstance(state, dict) else 'Not a dict'}")
                        
                        # Check for image data in state
                        if 'output_image' in state:
                            print(f"DEBUG: Found output_image in state")
                            self.display_session_image(state['output_image'], "Generated Visual Aid")
                        
                        if 'visual_aid_agent_output' in state:
                            print(f"DEBUG: Found visual_aid_agent_output in state")
                            visual_output = state['visual_aid_agent_output']
                            if isinstance(visual_output, dict) and 'image' in visual_output:
                                self.display_session_image(visual_output['image'], "Visual Aid from Agent")
                            elif isinstance(visual_output, str):
                                print(f"DEBUG: Visual aid output is string: {visual_output[:100]}...")
                else:
                    print(f"DEBUG: Could not get session details: {session_response.status_code}")
        except Exception as e:
            print(f"DEBUG: Error checking session artifacts: {e}")
            pass
    
    def display_session_image(self, image_data, caption="Generated Image"):
        """Display an image from session data"""
        try:
            print(f"DEBUG: Attempting to display image with caption: {caption}")
            print(f"DEBUG: Image data type: {type(image_data)}")
            
            if isinstance(image_data, str):
                # Try different base64 decoding approaches
                try:
                    # Remove data URL prefix if present
                    if image_data.startswith('data:image'):
                        header, data = image_data.split(',', 1)
                        image_data = data
                    
                    # Add padding if necessary
                    missing_padding = len(image_data) % 4
                    if missing_padding:
                        image_data += '=' * (4 - missing_padding)
                        print(f"DEBUG: Added {4 - missing_padding} padding characters")
                    
                    # Try direct base64 decode
                    image_bytes = base64.b64decode(image_data)
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption=caption, use_column_width=True)
                    print(f"DEBUG: Successfully displayed image: {caption}")
                    return True
                    
                except Exception as e:
                    print(f"DEBUG: Failed to decode image as base64: {e}")
                    print(f"DEBUG: Data preview: {image_data[:100]}...")
            
            elif isinstance(image_data, dict):
                # Handle different dictionary formats
                if 'data' in image_data:
                    try:
                        data = image_data['data']
                        
                        # Add padding if necessary
                        missing_padding = len(data) % 4
                        if missing_padding:
                            data += '=' * (4 - missing_padding)
                            
                        image_bytes = base64.b64decode(data)
                        image = Image.open(io.BytesIO(image_bytes))
                        st.image(image, caption=caption, use_column_width=True)
                        print(f"DEBUG: Successfully displayed image from dict: {caption}")
                        return True
                    except Exception as e:
                        print(f"DEBUG: Failed to decode image from dict: {e}")
                
                # Log the structure for debugging
                print(f"DEBUG: Image dict keys: {image_data.keys()}")
                print(f"DEBUG: Image dict content preview: {str(image_data)[:200]}...")
                
            else:
                print(f"DEBUG: Unknown image data format: {type(image_data)}")
                
        except Exception as e:
            print(f"DEBUG: Error in display_session_image: {e}")
            
        return False
    
    def fetch_artifact_image(self, session_id, filename):
        """Fetch and display image from artifacts endpoint"""
        try:
            artifact_url = f"{self.adk_base_url}/apps/sahayakai/users/streamlit_user/sessions/{session_id}/artifacts/{filename}"
            print(f"DEBUG: Fetching artifact from: {artifact_url}")
            
            response = requests.get(artifact_url)
            if response.status_code == 200:
                json_data = response.json()
                print(f"DEBUG: Artifact response keys: {json_data.keys()}")
                
                if 'inlineData' in json_data:
                    inline_data = json_data['inlineData']
                    print(f"DEBUG: InlineData keys: {inline_data.keys()}")
                    
                    # Check for mimeType
                    mime_type = inline_data.get('mimeType', 'unknown')
                    print(f"DEBUG: MIME type: {mime_type}")
                    
                    if 'data' in inline_data:
                        image_data = inline_data['data']
                        print(f"DEBUG: Found image data, length: {len(image_data)}")
                        
                        # Handle base64 decoding with proper padding
                        try:
                            # Clean the base64 data first - remove any non-base64 characters
                            import re
                            cleaned_data = re.sub(r'[^A-Za-z0-9+/=]', '', image_data)
                            print(f"DEBUG: Cleaned data length: {len(cleaned_data)} (removed {len(image_data) - len(cleaned_data)} chars)")
                            
                            # Remove any existing padding
                            cleaned_data = cleaned_data.rstrip('=')
                            
                            # Use a more robust approach for padding
                            remainder = len(cleaned_data) % 4
                            if remainder:
                                # Add the exact number of padding chars needed
                                padding_needed = 4 - remainder
                                cleaned_data += '=' * padding_needed
                                print(f"DEBUG: Added {padding_needed} padding characters, final length: {len(cleaned_data)}")
                            
                            # Use codecs for more robust decoding
                            import codecs
                            try:
                                # Try standard base64 first
                                decoded_data = base64.b64decode(cleaned_data)
                            except Exception:
                                # If that fails, try with codecs
                                decoded_data = codecs.decode(cleaned_data.encode('ascii'), 'base64')
                            
                            print(f"DEBUG: Decoded data length: {len(decoded_data)}")
                            
                            # Check the first few bytes to identify format
                            if len(decoded_data) >= 8:
                                header = decoded_data[:8]
                                print(f"DEBUG: Image header bytes: {[hex(b) for b in header]}")
                                
                                # Check for common image format signatures
                                if header.startswith(b'\x89PNG\r\n\x1a\n'):
                                    print("DEBUG: Detected PNG format")
                                elif header.startswith(b'\xff\xd8\xff'):
                                    print("DEBUG: Detected JPEG format")
                                elif header.startswith(b'GIF'):
                                    print("DEBUG: Detected GIF format")
                                else:
                                    print("DEBUG: Unknown image format")
                            
                            # Try to open as image
                            image = Image.open(io.BytesIO(decoded_data))
                            st.image(image, caption=f"Generated Visual Aid: {filename}", use_column_width=True)
                            print(f"DEBUG: Successfully displayed artifact image: {filename}")
                            return True
                            
                        except Exception as decode_error:
                            print(f"DEBUG: Base64 decode error: {decode_error}")
                            
                            # Try alternative: decode as bytes and write to temporary file
                            try:
                                # Use validate=False to be more lenient with corrupted data
                                original_data = inline_data['data']
                                
                                # Clean and try with validate=False
                                import re
                                cleaned = re.sub(r'[^A-Za-z0-9+/=]', '', original_data)
                                cleaned = cleaned.rstrip('=')
                                remainder = len(cleaned) % 4
                                if remainder:
                                    cleaned += '=' * (4 - remainder)
                                
                                decoded_data = base64.b64decode(cleaned, validate=False)
                                image = Image.open(io.BytesIO(decoded_data))
                                st.image(image, caption=f"Generated Visual Aid: {filename}", use_column_width=True)
                                st.success("✅ Visual aid displayed successfully!")
                                print(f"DEBUG: Successfully displayed image with validate=False: {filename}")
                                return True
                                
                            except Exception as alt_error:
                                print(f"DEBUG: Alternative decode failed: {alt_error}")
                                
                                # Final fallback: truncate to valid length
                                try:
                                    cleaned = re.sub(r'[^A-Za-z0-9+/=]', '', original_data)
                                    valid_length = (len(cleaned) // 4) * 4
                                    truncated = cleaned[:valid_length]
                                    
                                    decoded_data = base64.b64decode(truncated)
                                    image = Image.open(io.BytesIO(decoded_data))
                                    st.image(image, caption=f"Generated Visual Aid: {filename} (truncated)", use_column_width=True)
                                    st.warning("⚠️ Visual aid displayed with partial data - may be incomplete")
                                    print(f"DEBUG: Successfully displayed truncated image: {filename}")
                                    return True
                                    
                                except Exception as final_error:
                                    print(f"DEBUG: Final fallback failed: {final_error}")
                            
                            # Last resort: show error with debug info
                            print(f"DEBUG: Image data preview: {inline_data['data'][:100]}...")
                            st.error(f"❌ Could not decode image {filename} - the visual aid data appears to be corrupted")
                            return False
                            
                    else:
                        print(f"DEBUG: No 'data' key in inlineData")
                else:
                    print(f"DEBUG: No inlineData found in artifact response")
                    print(f"DEBUG: Available keys: {json_data.keys()}")
            else:
                print(f"DEBUG: Failed to fetch artifact, status: {response.status_code}")
                
        except Exception as e:
            print(f"DEBUG: Error fetching artifact {filename}: {e}")
            
        return False
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
    
    .sidebar-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
    }
    
    .sidebar-header h2 {
        margin: 0 0 0.5rem 0;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .sidebar-header p {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .main-header h1 {
        margin: 0 0 0.5rem 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0;
        font-size: 1.1rem;
        opacity: 0.9;
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
    
    /* Fix sidebar section headings alignment */
    .sidebar .element-container h3 {
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* Fix main page section headings alignment */
    .main .element-container h2 {
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 1.5rem;
        font-weight: 600;
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
        response = requests.get("http://localhost:8000/", timeout=5)
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
        # Display text content
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>Sahayak AI:</strong><br>
            {content.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        # Note: Images are now handled directly in format_adk_response method
        # This ensures they appear immediately when the response is processed

def clear_chat():
    """Clear the chat history"""
    st.session_state.messages = []
    # Also clear the session to start fresh
    if hasattr(st.session_state, 'adk_session_id'):
        del st.session_state.adk_session_id

def get_agent_info() -> Optional[Dict]:
    """Get information about the available agents"""
    try:
        response = requests.get("http://localhost:8000/list-apps", timeout=5)
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
    <div class="sidebar-header">
        <h2>🎓 Sahayak AI</h2>
        <p>Your Educational Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status check
    st.markdown("### 🔌 Connection Status")
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
    
    # Conversation Stats
    st.markdown("### 📊 Conversation Stats")
    st.info(get_conversation_stats())
    
    # Controls
    st.markdown("### 🛠️ Controls")
    
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



# Chat interface
st.markdown("## 💬 Chat with Sahayak AI")

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


