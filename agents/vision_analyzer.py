"""
Vision Analyzer Agent - Analyzes body photos to assess physique and create personalized plans
"""
import os
import base64
import requests
from pathlib import Path


def encode_image_to_base64(image_path):
    """
    Convert image file to base64 string for API

    Args:
        image_path: Path to image file

    Returns:
        str: Base64 encoded image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def call_nemotron_vision(prompt, image_path=None, image_base64=None, system_prompt=""):
    """
    Call NVIDIA NIM API with Nemotron vision model

    Args:
        prompt: The user prompt
        image_path: Path to image file (optional)
        image_base64: Base64 encoded image (optional)
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

    # Prepare image
    if image_path and not image_base64:
        image_base64 = encode_image_to_base64(image_path)

    # Build message content with image
    content = []
    if image_base64:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}"
            }
        })
    content.append({
        "type": "text",
        "text": prompt
    })

    body = {
        "model": "nvidia/nemotron-nano-12b-v2-vl",
        "messages": [
            {"role": "system", "content": system_prompt or "You are an expert fitness coach and body composition analyst."},
            {"role": "user", "content": content}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }

    try:
        r = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=45
        )
        r.raise_for_status()
        response_data = r.json()
        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response")

    except requests.exceptions.RequestException as e:
        return f"⚠️  API Error: {str(e)}"


def analyze_physique(image_path=None, image_base64=None, user_goals="build muscle"):
    """
    Analyze body photo to assess current physique and fitness level

    Args:
        image_path: Path to body photo
        image_base64: Base64 encoded image
        user_goals: User's fitness goals

    Returns:
        str: Detailed physique analysis
    """
    system_prompt = """You are an expert personal trainer and body composition specialist.
    Analyze physique photos professionally and provide constructive, actionable feedback.
    Focus on muscle development, body composition, posture, and areas for improvement."""

    prompt = f"""Analyze this physique photo and provide a comprehensive assessment:

User's Goal: {user_goals}

Please analyze:
1. **Current Body Composition**: Estimated body fat percentage range, muscle mass distribution
2. **Muscle Development**: Which muscle groups are well-developed, which need focus
3. **Symmetry & Balance**: Any muscle imbalances or asymmetries to address
4. **Posture & Form**: Any postural issues that could affect training
5. **Starting Point Classification**: Beginner/Intermediate/Advanced lifter assessment
6. **Key Strengths**: What they're doing right
7. **Priority Areas**: Top 3 muscle groups to focus on for their goal

Be encouraging but honest. Provide specific, actionable insights."""

    return call_nemotron_vision(prompt, image_path, image_base64, system_prompt)


def create_visual_workout_plan(physique_analysis, user_data):
    """
    Create a customized workout plan based on visual physique analysis

    Args:
        physique_analysis: Analysis from analyze_physique()
        user_data: Additional user data (goals, experience, etc.)

    Returns:
        str: Personalized workout plan
    """
    system_prompt = """You are an expert strength coach who creates scientifically-backed,
    personalized workout programs based on individual physique assessments."""

    prompt = f"""Based on this physique analysis, create a detailed workout program:

PHYSIQUE ANALYSIS:
{physique_analysis}

USER INFO:
- Goal: {user_data.get('goal', 'build muscle')}
- Experience: {user_data.get('experience', 'intermediate')}
- Available Days: {user_data.get('days_per_week', 4)} days/week
- Body Weight: {user_data.get('body_weight', 'unknown')} lbs

Create a complete program with:

1. **TRAINING SPLIT** (which days for which muscle groups)
2. **EXERCISE SELECTION** (5-7 exercises per session)
   - Primary compound movements
   - Accessory exercises targeting weak points from analysis
3. **VOLUME & INTENSITY**
   - Sets x Reps for each exercise
   - Progressive overload strategy
4. **WEEK-BY-WEEK PROGRESSION** (next 4 weeks)
5. **KEY FOCUS AREAS** based on the physique analysis

Make it specific, progressive, and directly address the physique assessment findings."""

    return call_nemotron_vision(prompt, system_prompt=system_prompt)


def assess_progress_from_photos(before_image, after_image, weeks_between):
    """
    Compare before/after photos to assess progress

    Args:
        before_image: Path or base64 of before photo
        after_image: Path or base64 of after photo
        weeks_between: Number of weeks between photos

    Returns:
        str: Progress assessment
    """
    system_prompt = """You are an expert at assessing fitness transformation progress.
    Compare before/after photos objectively and provide encouraging, specific feedback."""

    # For now, analyze the after image with context
    # In future, could send both images if API supports multiple images
    prompt = f"""Analyze this progress photo taken {weeks_between} weeks into a training program.

Assess the following:
1. **Visible Changes**: What muscle groups show noticeable development?
2. **Body Composition**: Any visible fat loss or muscle gain?
3. **Overall Progress**: Rate the transformation (considering the timeframe)
4. **Strengths**: What's working well in their program?
5. **Next Steps**: What to focus on for continued progress?

Timeframe: {weeks_between} weeks
Be specific and motivating. Celebrate wins and give actionable advice for continued improvement."""

    # Analyze the after image
    if isinstance(after_image, str) and os.path.exists(after_image):
        return call_nemotron_vision(prompt, image_path=after_image, system_prompt=system_prompt)
    else:
        return call_nemotron_vision(prompt, image_base64=after_image, system_prompt=system_prompt)


def suggest_form_corrections(exercise_image, exercise_name):
    """
    Analyze exercise form from photo/video frame

    Args:
        exercise_image: Path or base64 of exercise photo
        exercise_name: Name of the exercise being performed

    Returns:
        str: Form analysis and corrections
    """
    system_prompt = """You are a certified strength and conditioning coach specializing in
    proper exercise form and injury prevention."""

    prompt = f"""Analyze this photo of someone performing a {exercise_name}.

Assess:
1. **Current Form**: What are they doing correctly?
2. **Form Issues**: Any problems with technique, posture, or positioning?
3. **Injury Risks**: Potential injury risks from current form
4. **Corrections**: Step-by-step cues to improve form
5. **Safety Tips**: Key points to remember for this exercise

Be specific about body positioning, joint angles, and movement patterns."""

    if isinstance(exercise_image, str) and os.path.exists(exercise_image):
        return call_nemotron_vision(prompt, image_path=exercise_image, system_prompt=system_prompt)
    else:
        return call_nemotron_vision(prompt, image_base64=exercise_image, system_prompt=system_prompt)


if __name__ == "__main__":
    # Test the vision agent
    print("=== Testing Vision Analyzer Agent ===")
    print("\nNote: This requires an actual body photo to test.")
    print("Usage example:")
    print('  analysis = analyze_physique("path/to/photo.jpg", user_goals="build muscle")')
    print('  workout = create_visual_workout_plan(analysis, {"goal": "build muscle", "days_per_week": 4})')
