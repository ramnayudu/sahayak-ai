"""
Local Model Client for Sahayak AI - Transformer Lab Integration
Provides a wrapper to use local Gemma models with Transformer Lab
"""

import os
import requests
import json
from typing import Dict, Any, Optional, List
from . import config


class TransformerLabClient:
    """Client for communicating with Transformer Lab local models"""
    
    def __init__(self, base_url: str = None, model_name: str = None):
        self.base_url = base_url or config.LOCAL_MODEL_URL
        self.model_name = model_name or config.LOCAL_MODEL_NAME
        self.timeout = 60.0
        
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the Transformer Lab API."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Transformer Lab API: {e}")
    
    def get_conversation_template(self) -> Dict[str, Any]:
        """Get the conversation template for the model."""
        try:
            return self._make_request("worker_get_conv_template", {})
        except:
            # Fallback template
            return {
                "conv": {
                    "name": "gemma",
                    "roles": ["user", "model"],
                    "sep": "<end_of_turn>\n",
                    "stop_str": "<end_of_turn>"
                }
            }
    
    def generate_text(self, 
                     prompt: str, 
                     max_tokens: int = 256,
                     temperature: float = 0.7,
                     top_p: float = 0.9,
                     repetition_penalty: float = 1.2) -> str:  # Increased repetition penalty
        """Generate text using the local model."""
        
        # Try the working parameter format directly
        request_data = {
            "prompt": prompt,
            "max_new_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "repetition_penalty": repetition_penalty,
            "do_sample": True,
        }
        
        try:
            response = self._make_request("worker_generate", request_data)
            
            # Extract the generated text
            generated_text = response.get("text", "")
            
            if generated_text:
                # Remove the original prompt if it's echoed back
                if generated_text.startswith(prompt):
                    generated_text = generated_text[len(prompt):].strip()
                
                # Clean up common artifacts
                generated_text = generated_text.replace("<end_of_turn>", "")
                generated_text = generated_text.replace("<start_of_turn>", "")
                
                # Handle repetitive content by detecting patterns
                lines = generated_text.split('\n')
                unique_lines = []
                seen_lines = set()
                
                for line in lines:
                    line = line.strip()
                    if (line and 
                        line not in seen_lines and  # Remove exact duplicates
                        len(line) > 5 and  # Skip very short lines
                        not line.startswith('[User') and 
                        not line.startswith('User ') and
                        not line.startswith('[Assistant') and
                        not line == 'User:' and
                        not line == 'Assistant:'):
                        
                        unique_lines.append(line)
                        seen_lines.add(line)
                        
                        # Stop if we have enough content
                        if len(unique_lines) >= 3:
                            break
                
                if unique_lines:
                    # Join the unique lines
                    result = ' '.join(unique_lines)
                    
                    # Ensure complete sentences
                    sentences = result.split('. ')
                    if len(sentences) > 1 and not sentences[-1].endswith(('.', '!', '?')):
                        # Remove incomplete last sentence
                        result = '. '.join(sentences[:-1]) + '.'
                    
                    return result.strip()
                else:
                    # Fallback: take first paragraph and ensure it's complete
                    paragraphs = generated_text.split('\n\n')
                    if paragraphs:
                        first_para = paragraphs[0].strip()
                        sentences = first_para.split('. ')
                        if len(sentences) > 1 and not sentences[-1].endswith(('.', '!', '?')):
                            first_para = '. '.join(sentences[:-1]) + '.'
                        return first_para
            
            return "No response generated"
            
        except Exception as e:
            print(f"Error generating text with Transformer Lab: {e}")
            return f"Error: Could not generate response - {str(e)}"
    
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Process chat messages and generate a response.
        """
        # Convert messages to a single prompt
        prompt_parts = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt = "\n".join(prompt_parts)
        
        # Generate response
        response_text = self.generate_text(
            prompt=prompt,
            max_tokens=kwargs.get("max_tokens", 256),
            temperature=kwargs.get("temperature", 0.7),
            top_p=kwargs.get("top_p", 0.9)
        )
        
        return response_text


class LocalModelAdapter:
    """Adapter to make local model work with ADK Agent expectations"""
    
    def __init__(self):
        if config.USE_LOCAL_MODEL:
            self.client = TransformerLabClient()
        else:
            self.client = None
        
    def generate_content(self, prompt: str, **kwargs) -> str:
        """Generate content using local model, compatible with ADK expectations"""
        if self.client:
            return self.client.generate_text(prompt, **kwargs)
        else:
            raise Exception("Local model not configured")


# Global instance for use in agents
local_model_adapter = LocalModelAdapter() if config.USE_LOCAL_MODEL else None


def get_model_client():
    """Get the appropriate model client based on configuration"""
    if config.USE_LOCAL_MODEL:
        return local_model_adapter
    else:
        # Return None to use default ADK/Vertex AI client
        return None
