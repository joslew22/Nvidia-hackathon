#!/usr/bin/env python3
"""Test NVIDIA API connection"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NIM_API_KEY")
print(f"API Key found: {api_key[:20]}..." if api_key else "No API key found!")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

body = {
    "model": "nvidia/nemotron-nano-12b-v2-vl",
    "messages": [
        {"role": "user", "content": "Say hello in 5 words"}
    ],
    "max_tokens": 20,
    "temperature": 0.5
}

print("\nTesting API connection...")
print(f"Endpoint: https://integrate.api.nvidia.com/v1/chat/completions")
print(f"Model: {body['model']}\n")

try:
    response = requests.post(
        "https://integrate.api.nvidia.com/v1/chat/completions",
        headers=headers,
        json=body,
        timeout=30,
        verify=True  # Ensure SSL verification
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}\n")

    if response.status_code == 200:
        data = response.json()
        print("✅ SUCCESS!")
        print(f"Response: {data}")
        if "choices" in data:
            print(f"\nMessage: {data['choices'][0]['message']['content']}")
    else:
        print(f"❌ Error {response.status_code}")
        print(f"Response: {response.text}")

except requests.exceptions.SSLError as e:
    print(f"❌ SSL Error: {e}")
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection Error: {e}")
except requests.exceptions.Timeout as e:
    print(f"❌ Timeout Error: {e}")
except Exception as e:
    print(f"❌ Unexpected Error: {type(e).__name__}: {e}")
