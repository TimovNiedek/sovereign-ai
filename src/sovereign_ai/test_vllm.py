#!/usr/bin/env python3
"""
Test script to verify vLLM is working correctly with the API.
"""

import os
import requests
from typing import Dict, Any

def test_vllm_api():
    """Test if vLLM API is accessible and responding."""
    
    # Configuration
    base_url = "http://localhost:8000/v1"
    api_key = ""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Check if the API is reachable
    try:
        response = requests.get(f"{base_url}/models", headers=headers)
        if response.status_code == 200:
            print("✓ vLLM API is accessible")
            models = response.json()
            print(f"Available models: {models}")
        else:
            print(f"✗ Failed to reach vLLM API: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Failed to connect to vLLM API: {e}")
        return False
    
    # Test 2: Simple chat completion
    try:
        payload = {
            "model": "qwen3-coder-30B-A3B-Instruct-AWQ",
            "messages": [
                {"role": "user", "content": "Hello, world!"}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Chat completion successful")
            print(f"Response: {result['choices'][0]['message']['content'][:100]}...")
        else:
            print(f"✗ Chat completion failed: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"✗ Chat completion test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing vLLM setup...")
    success = test_vllm_api()
    if success:
        print("\n✓ All tests passed! vLLM is working correctly.")
    else:
        print("\n✗ Some tests failed.")