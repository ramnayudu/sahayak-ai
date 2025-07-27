#!/usr/bin/env python3
"""
Test script to discover and test local model endpoints
"""

import asyncio
import httpx
import json

async def test_local_model_endpoints():
    """Test various common endpoints for local LLM servers"""
    
    base_url = "http://localhost:21002"
    
    # Common endpoints to test
    endpoints = [
        # OpenAI compatible
        ("/v1/models", "GET", None),
        ("/v1/chat/completions", "POST", {
            "model": "google/gemma-3-1b-pt",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10
        }),
        ("/v1/completions", "POST", {
            "model": "google/gemma-3-1b-pt", 
            "prompt": "Hello",
            "max_tokens": 10
        }),
        
        # Ollama style
        ("/api/generate", "POST", {
            "model": "google/gemma-3-1b-pt",
            "prompt": "Hello",
            "stream": False
        }),
        ("/api/chat", "POST", {
            "model": "google/gemma-3-1b-pt",
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": False
        }),
        
        # Generic endpoints
        ("/generate", "POST", {
            "prompt": "Hello",
            "max_tokens": 10
        }),
        ("/completion", "POST", {
            "prompt": "Hello",
            "max_length": 10
        }),
        ("/predict", "POST", {
            "text": "Hello",
            "max_tokens": 10
        }),
        
        # Info endpoints
        ("/", "GET", None),
        ("/health", "GET", None),
        ("/models", "GET", None),
        ("/info", "GET", None),
        ("/docs", "GET", None),
        ("/openapi.json", "GET", None),
    ]
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        print(f"Testing endpoints on {base_url}...")
        print("=" * 60)
        
        working_endpoints = []
        
        for endpoint, method, payload in endpoints:
            url = f"{base_url}{endpoint}"
            try:
                if method == "GET":
                    response = await client.get(url)
                else:  # POST
                    response = await client.post(
                        url,
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                
                print(f"{method} {endpoint}: {response.status_code}")
                
                if response.status_code == 200:
                    working_endpoints.append((endpoint, method, payload))
                    try:
                        content = response.json()
                        if len(str(content)) < 500:  # Only show short responses
                            print(f"  Response: {content}")
                        else:
                            print(f"  Response: [Large response - {len(str(content))} chars]")
                    except:
                        print(f"  Response: [Non-JSON content]")
                elif response.status_code == 404:
                    print(f"  Status: Not Found")
                elif response.status_code == 422:
                    print(f"  Status: Validation Error (endpoint exists but wrong format)")
                    working_endpoints.append((endpoint, method, "needs_different_format"))
                else:
                    print(f"  Status: {response.status_code}")
                    
            except httpx.ConnectError:
                print(f"{method} {endpoint}: Connection Error")
                break
            except httpx.TimeoutException:
                print(f"{method} {endpoint}: Timeout")
            except Exception as e:
                print(f"{method} {endpoint}: Error - {str(e)}")
        
        print("\n" + "=" * 60)
        print("WORKING ENDPOINTS:")
        for endpoint, method, payload in working_endpoints:
            print(f"  {method} {endpoint}")
        
        return working_endpoints

if __name__ == "__main__":
    asyncio.run(test_local_model_endpoints())
