#!/usr/bin/env python3
"""
Test script to verify vLLM is working correctly with the API.
"""

import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def test_litellm_api():
    """Test if LiteLLM API is accessible and responding."""

    # Configuration
    base_url = "http://localhost:4000/v1"
    api_key = os.getenv("LITELLM_MASTER_KEY", "")
    profile = os.getenv("PROFILE", "local")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    models: Dict[str, Any] = {}

    # Test 1: Check if the API is reachable
    try:
        response = requests.get(f"{base_url}/models", headers=headers)
        if response.status_code == 200:
            print("✓ LiteLLM API is accessible")
            models = response.json()
            print(f"Available models: {models}")
        else:
            print(f"✗ Failed to reach LiteLLM API: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Failed to connect to LiteLLM API: {e}")
        return False

    if not models.get("data"):
        print("✗ No models available in LiteLLM")
        return False

    # Test 2: Simple chat completion
    failures = 0
    for model in models["data"]:
        model_id = model.get("id")
        print(f"Testing model: {model_id}")
        try:
            payload = {
                "model": model_id,
                "messages": [{"role": "user", "content": "Hello, world!"}],
                "temperature": 0.7,
                "max_tokens": 100,
            }

            response = requests.post(
                f"{base_url}/chat/completions", json=payload, headers=headers
            )

            if response.status_code == 200:
                result = response.json()
                print("✓ Chat completion successful")
                print(
                    f"Response: {result['choices'][0]['message']['content'][:100]}..."
                )
            else:
                print(f"✗ Chat completion failed: {response.status_code}")
                print(response.text)
                failures += 1

        except Exception as e:
            print(f"✗ Chat completion test failed: {e}")
            failures += 1

    return failures == 0


if __name__ == "__main__":
    print("Testing LiteLLM setup...")
    success = test_litellm_api()
    if success:
        print("\n✓ All tests passed! LiteLLM is working correctly.")
    else:
        print("\n✗ Some tests failed.")
