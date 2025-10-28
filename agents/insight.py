"""
Insight Agent - Analyzes user data to identify patterns and improvement areas
"""
import os
import requests
import json


def call_nemotron(prompt, system_prompt=""):
    """
    Call NVIDIA NIM API with Nemotron model

    Args:
        prompt: The user prompt
        system_prompt: Optional system instruction

    Returns:
        str: The model's response
    """
    api_key = os.getenv("NIM_API_KEY")
    if not api_key:
        return "⚠️  NIM_API_KEY not found. Please set it in your .env file."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Adjust the endpoint and payload based on actual NVIDIA NIM API spec
    # This is a template structure
    body = {
        "model": "nemotron",
        "messages": [
            {"role": "system", "content": system_prompt or "You are an AI wellness insight analyst."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        r = requests.post(
            "https://api.nvidia.com/v1/nim/invoke",
            headers=headers,
            json=body,
            timeout=30
        )
        r.raise_for_status()
        response_data = r.json()

        # Adjust based on actual API response structure
        return response_data.get("output", response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response"))

    except requests.exceptions.RequestException as e:
        return f"⚠️  API Error: {str(e)}"


def analyze_user(data):
    """
    Analyze user wellness data and provide insights

    Args:
        data: Dictionary containing user wellness metrics

    Returns:
        str: Analysis insights
    """
    system_prompt = """You are a wellness insight analyst specializing in digital wellbeing
    and healthy habits. Analyze user data objectively and identify key patterns,
    particularly around screen time and health behaviors."""

    prompt = f"""Analyze this user's wellness data and provide 3-5 brief insights:

User Data:
- Screen scrolling time: {data.get('scroll_minutes', 0)} minutes
- Gym/Exercise completed: {data.get('gym_done', False)}
- Current mood: {data.get('mood', 'unknown')}
- Sleep hours: {data.get('sleep_hours', 'unknown')}
- Water intake (glasses): {data.get('water_intake', 'unknown')}
- Screen time breaks taken: {data.get('screen_time_breaks', 0)}

Focus on:
1. Doomscrolling/excessive screen time patterns
2. Connection between behaviors (sleep, exercise, mood)
3. Key improvement areas
4. What they're doing well

Keep it concise and actionable."""

    return call_nemotron(prompt, system_prompt)


if __name__ == "__main__":
    # Test the agent
    sample_data = {
        "scroll_minutes": 90,
        "gym_done": False,
        "mood": "tired",
        "sleep_hours": 5.5,
        "water_intake": 3,
        "screen_time_breaks": 1
    }

    print("=== Testing Insight Agent ===")
    result = analyze_user(sample_data)
    print(result)
