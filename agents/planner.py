"""
Planner Agent - Creates actionable next-day plans based on insights
"""
import os
import requests


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

    body = {
        "model": "nemotron",
        "messages": [
            {"role": "system", "content": system_prompt or "You are a strategic wellness planner."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.6,
        "max_tokens": 400
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
        return response_data.get("output", response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response"))

    except requests.exceptions.RequestException as e:
        return f"⚠️  API Error: {str(e)}"


def plan_next_day(insights, user_data=None):
    """
    Create a realistic plan for tomorrow based on insights

    Args:
        insights: Analysis from the Insight Agent
        user_data: Optional raw user data for context

    Returns:
        str: Actionable plan for the next day
    """
    system_prompt = """You are a strategic wellness planner who creates realistic,
    achievable daily plans. Focus on small, incremental improvements that fit naturally
    into someone's routine. Prioritize reducing screen time and building healthy habits."""

    user_context = ""
    if user_data:
        user_context = f"""
Current patterns:
- Daily scroll time: {user_data.get('scroll_minutes', 'unknown')} minutes
- Exercise habit: {'Active' if user_data.get('gym_done') else 'Inactive'}
- Sleep quality: {user_data.get('sleep_hours', 'unknown')} hours
"""

    prompt = f"""Based on these insights, create a simple plan for tomorrow:

Insights:
{insights}
{user_context}

Create a plan with:
1. ONE specific screen time reduction strategy (with exact time/app limits)
2. ONE physical activity or wellness action (be specific about when/how)
3. ONE small habit to support better sleep or focus

Make each action:
- Specific (exact times, durations, or triggers)
- Realistic (fits into a normal day)
- Measurable (clear success criteria)

Format as a brief bullet list."""

    return call_nemotron(prompt, system_prompt)


if __name__ == "__main__":
    # Test the agent
    sample_insights = "User scrolls 90 mins daily, misses exercise, low sleep affects mood."
    sample_data = {
        "scroll_minutes": 90,
        "gym_done": False,
        "sleep_hours": 5.5
    }

    print("=== Testing Planner Agent ===")
    result = plan_next_day(sample_insights, sample_data)
    print(result)
