"""
Planner Agent - Creates actionable next-day plans based on insights
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def call_nemotron(prompt, system_prompt=""):
    """
    Call NVIDIA NIM API with recommended workout planning model

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
            {"role": "system", "content": system_prompt or "You are a master strength and conditioning coach who creates detailed, progressive workout plans."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.6,
        "max_tokens": 800,
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
        return f"⚠️  API Error: {str(e)}"


def plan_next_day(insights, user_data=None):
    """
    Create a detailed workout and nutrition plan for tomorrow

    Args:
        insights: Analysis from the Insight Agent
        user_data: Optional raw user data for context

    Returns:
        str: Actionable workout and meal plan for the next day
    """
    # Import knowledge base
    try:
        from knowledge_base import get_relevant_knowledge, PROGRESSIVE_OVERLOAD, RECOVERY_NUTRITION
        has_knowledge = True
    except:
        has_knowledge = False

    system_prompt = """You are an expert strength and conditioning coach who creates
    progressive workout plans and meal prep strategies. Focus on progressive overload,
    proper recovery, and nutrition timing to maximize gains."""

    user_context = ""
    if user_data:
        max_lifts = user_data.get('max_lifts', {})
        recent_lifts = user_data.get('recent_lifts', {})

        user_context = f"""
Current Stats:
- Workout completed: {'Yes' if user_data.get('workout_done') else 'No'}
- Last workout: {user_data.get('workout_type', 'unknown')}
- Max lifts: {max_lifts}
- Recent workout weights: {recent_lifts}
- Protein intake: {user_data.get('protein_grams', 'unknown')}g
- Sleep: {user_data.get('sleep_hours', 'unknown')} hours
- Soreness: {user_data.get('soreness', 'unknown')}/10
- Energy: {user_data.get('energy', 'unknown')}
"""

    # Add expert knowledge to prompt
    knowledge_context = ""
    if has_knowledge:
        knowledge_context = f"""
EXPERT KNOWLEDGE BASE:
{PROGRESSIVE_OVERLOAD}

{RECOVERY_NUTRITION}

Use this expert knowledge to create scientifically-backed recommendations.
"""

    prompt = f"""{knowledge_context}

Based on these insights, create tomorrow's workout and nutrition plan:

Insights:
{insights}
{user_context}

Create a detailed plan with:

1. WORKOUT PLAN:
   - Specific exercises with sets x reps
   - Target weights (based on progressive overload - suggest 2.5-5lb increases if ready)
   - Estimated time and when to train
   - Rest periods between sets

2. MEAL PREP PLAN:
   - Protein target for the day (based on body weight)
   - 3-4 specific meal ideas with rough macros
   - Pre/post workout nutrition timing
   - Water intake goal

3. RECOVERY ACTIONS:
   - Sleep target
   - Stretching/mobility work
   - Active recovery suggestions if sore

Make it specific, measurable, and progressive. If suggesting weight increases, explain why they're ready."""

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
