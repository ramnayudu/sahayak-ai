#!/usr/bin/env python3
"""
Debug script to test Transformer Lab responses
"""

import requests
import json

def test_transformer_lab_direct():
    """Test Transformer Lab API directly with various prompts"""
    
    url = "http://localhost:21002/worker_generate"
    
    test_prompts = [
        "Hello, how are you?",
        "Tell me a story about a cat.",
        "What is 2+2?",
        "Create a simple math problem for children.",
        "Once upon a time, there was a farmer who",
    ]
    
    for prompt in test_prompts:
        print(f"\n{'='*50}")
        print(f"PROMPT: {prompt}")
        print(f"{'='*50}")
        
        request_data = {
            "prompt": prompt,
            "max_new_tokens": 100,
            "temperature": 0.7,
            "top_p": 0.9,
            "repetition_penalty": 1.0,
            "do_sample": True,
        }
        
        try:
            response = requests.post(
                url, 
                json=request_data, 
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("text", "")
                print(f"RAW RESPONSE: {repr(generated_text)}")
                print(f"RESPONSE: {generated_text}")
                
                # Show length
                print(f"LENGTH: {len(generated_text)} characters")
                
            else:
                print(f"ERROR: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"EXCEPTION: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_transformer_lab_direct()
