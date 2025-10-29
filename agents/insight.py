"""
Insight Agent - Analyzes user data to identify patterns and improvement areas
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def call_nemotron(prompt, system_prompt=""):
    """
    Call NVIDIA NIM API with recommended fitness coaching model

    Args:
        prompt: The user prompt
        system_prompt: Optional system instruction

    Returns:
        str: The model's response
    """
    api_key = os.getenv("NIM_API_KEY")
    if not api_key:
        return "⚠️  NIM_API_KEY not found. Please set it in your .env file."

    # Get model configuration from environment
    model = os.getenv("INSIGHT_MODEL", "nvidia/nemotron-4-340b-instruct")
    fallback_model = os.getenv("FALLBACK_MODEL", "nvidia/llama-3.1-nemotron-70b-instruct")
    endpoint = os.getenv("NIM_ENDPOINT", "https://integrate.api.nvidia.com/v1")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt or "You are an expert fitness analyst specializing in strength training and progressive overload."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 600,
        "top_p": 0.9
    }

    try:
        # Try primary model first
        r = requests.post(
            f"{endpoint}/chat/completions",
            headers=headers,
            json=body,
            timeout=45
        )
        r.raise_for_status()
        response_data = r.json()

        # Extract response from NVIDIA API format
        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response")

    except requests.exceptions.RequestException as e:
        # Try fallback model if primary fails
        try:
            body["model"] = fallback_model
            r = requests.post(
                f"{endpoint}/chat/completions",
                headers=headers,
                json=body,
                timeout=30
            )
            r.raise_for_status()
            response_data = r.json()
            return response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        except:
            return f"⚠️  API Error: {str(e)}"


def analyze_user(data):
    """
    Analyze user fitness data and provide insights

    Args:
        data: Dictionary containing user fitness metrics

    Returns:
        str: Analysis insights
    """
    # Import knowledge base for better analysis
    try:
        from knowledge_base import PROGRESSIVE_OVERLOAD, RECOVERY_NUTRITION
        knowledge_context = f"""
EXPERT KNOWLEDGE FOR ANALYSIS:
{PROGRESSIVE_OVERLOAD}

{RECOVERY_NUTRITION}

Use these scientific principles to analyze the user's readiness for training.
"""
    except:
        knowledge_context = ""

    system_prompt = """You are a fitness and strength training analyst specializing in
    progressive overload, nutrition, and workout optimization. Analyze user data objectively
    and identify patterns in their training, recovery, and nutrition."""

    # Include photo analysis if available
    photo_section = ""
    if data.get('photo_analysis'):
        photo_section = f"""

PHYSIQUE ANALYSIS FROM PHOTO:
{data.get('photo_analysis')}
"""

    prompt = f"""{knowledge_context}

Analyze this user's fitness data and provide 3-5 key insights:

User Data:
- Workout completed: {data.get('workout_done', False)}
- Workout type: {data.get('workout_type', 'unknown')}
- Current max lifts: {data.get('max_lifts', {})}
- Recent workout weights: {data.get('recent_lifts', {})}
- Protein intake (g): {data.get('protein_grams', 'unknown')}
- Total calories: {data.get('calories', 'unknown')}
- Sleep hours: {data.get('sleep_hours', 'unknown')}
- Water intake (oz): {data.get('water_oz', 'unknown')}
- Soreness level (1-10): {data.get('soreness', 'unknown')}
- Energy level: {data.get('energy', 'unknown')}
{photo_section}

Focus on:
1. Training consistency and progressive overload opportunities
2. Recovery indicators (sleep, soreness, energy)
3. Nutrition adequacy for fitness goals (protein, calories)
4. Strength progression and readiness to increase weight
5. If photo analysis is provided, incorporate those physique insights into recommendations
6. What they're doing well

Keep it concise, specific, and actionable."""

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
