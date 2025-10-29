"""
Coach Agent - Provides motivational feedback and actionable advice
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def call_nemotron(prompt, system_prompt=""):
    """
    Call NVIDIA NIM API with recommended motivational coaching model

    Args:
        prompt: The user prompt
        system_prompt: Optional system instruction

    Returns:
        str: The model's response
    """
    api_key = os.getenv("NIM_API_KEY")
    if not api_key:
        return "⚠️  NIM_API_KEY not found. Please set it in your .env file."

    # Use the model from your API key
    model = "nvidia/nemotron-nano-12b-v2-vl"
    endpoint = "https://integrate.api.nvidia.com/v1"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt or "You are an elite strength coach and motivator who inspires lifters to reach their potential."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
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


def motivate_user(insights, plan=""):
    """
    Provide motivational coaching and lifting progression advice

    Args:
        insights: Analysis from the Insight Agent
        plan: Suggested plan from the Planner Agent (optional)

    Returns:
        str: Motivational coaching message with progression guidance
    """
    system_prompt = """You are a hardcore strength coach and motivator who helps lifters
    push past plateaus and reach new PRs. You understand progressive overload, periodization,
    and the mental game of lifting. You're supportive but push people to their potential.
    Be energetic, confident, and inspiring."""

    prompt = f"""Based on these insights and workout plan, provide powerful motivation and coaching:

Insights:
{insights}

Tomorrow's Plan:
{plan if plan else "None yet"}

Provide:
1. HYPE THEM UP - Celebrate wins and acknowledge their hard work
2. PR POTENTIAL - If they're ready for a weight increase, explain the science and get them excited
3. MINDSET - One powerful mental strategy for crushing tomorrow's workout
4. ACCOUNTABILITY - A specific challenge or goal to hit

Be intense, motivating, and specific. Use lifting terminology. Make them want to destroy that workout.
If their recovery isn't optimal (low sleep, high soreness), advise scaling back intelligently.

End with a powerful one-liner that'll fire them up."""

    return call_nemotron(prompt, system_prompt)


if __name__ == "__main__":
    # Test the agent
    sample_insights = "User is scrolling 90 mins/day. Sleep is low. Needs more breaks."
    sample_plan = "Tomorrow: 30-min morning walk, set phone timer for 20-min work blocks."

    print("=== Testing Coach Agent ===")
    result = motivate_user(sample_insights, sample_plan)
    print(result)
