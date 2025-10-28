"""
Coach Agent - Provides motivational feedback and actionable advice
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
            {"role": "system", "content": system_prompt or "You are a supportive wellness coach."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
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


def motivate_user(insights, plan=""):
    """
    Provide positive, realistic coaching based on insights and plan

    Args:
        insights: Analysis from the Insight Agent
        plan: Suggested plan from the Planner Agent (optional)

    Returns:
        str: Motivational coaching message
    """
    system_prompt = """You are an empathetic wellness coach focused on positive reinforcement
    and realistic, achievable actions. You help users overcome doomscrolling and build
    sustainable healthy habits. Be encouraging but honest."""

    prompt = f"""Based on these insights and planned actions, provide motivational coaching:

Insights:
{insights}

Planned Actions:
{plan if plan else "None yet"}

Provide:
1. Positive reinforcement for what they're doing well
2. One realistic, specific action they can take TODAY
3. A brief encouraging message (2-3 sentences max)

Keep your tone warm, supportive, and action-oriented."""

    return call_nemotron(prompt, system_prompt)


if __name__ == "__main__":
    # Test the agent
    sample_insights = "User is scrolling 90 mins/day. Sleep is low. Needs more breaks."
    sample_plan = "Tomorrow: 30-min morning walk, set phone timer for 20-min work blocks."

    print("=== Testing Coach Agent ===")
    result = motivate_user(sample_insights, sample_plan)
    print(result)
