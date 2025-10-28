# 🎓 Training & Fine-tuning Guide for FocusFlow

## Overview

While we're using NVIDIA's pre-trained Nemotron model, there are several ways to improve performance and customize responses for fitness coaching.

## 1. 🎯 Prompt Engineering (Easiest - Already Using)

### What We're Doing Now:
```python
system_prompt = """You are a hardcore strength coach and motivator who helps lifters
push past plateaus and reach new PRs. You understand progressive overload, periodization,
and the mental game of lifting."""
```

### How to Improve:

**A. Add Few-Shot Examples**
```python
system_prompt = """You are an expert fitness coach.

Example 1:
User: Bench 185x5, sleep 8hrs, soreness 3/10
You: Great recovery! Time to push for 190x5. Your CNS is fresh.

Example 2:
User: Bench 185x5, sleep 5hrs, soreness 8/10
You: Recovery is compromised. Drop to 175x5 today, focus on form.

Now analyze this user:
"""
```

**B. Add Domain-Specific Context**
```python
context = """
PROGRESSIVE OVERLOAD PRINCIPLES:
- Increase weight by 2.5-5lbs when you hit target reps for 2 consecutive sessions
- Deload every 4-6 weeks (reduce volume by 40%)
- Prioritize compound movements: Squat, Bench, Deadlift, OHP

RECOVERY INDICATORS:
- Sleep <6hrs = reduce volume 20%
- Soreness >7/10 = active recovery or rest
- Sleep >8hrs + soreness <4 = optimal for PR attempts

NUTRITION TARGETS:
- Protein: 0.8-1g per lb bodyweight
- Muscle gain: +300-500 cal surplus
- Fat loss: -300-500 cal deficit
"""
```

**C. Use Retrieval Augmented Generation (RAG)**
```python
def get_relevant_context(user_query):
    """Pull relevant info from knowledge base"""
    knowledge_base = {
        "bench_press": {
            "form": "Bar path straight down to mid-chest, elbows 45 degrees",
            "progression": "Add 2.5lbs when you hit 3x5 with good form",
            "assistance": "Close-grip bench, dips, tricep work"
        },
        "squat": {
            "form": "Depth to parallel or below, knees track over toes",
            "progression": "Add 5lbs when you hit 3x5 with depth",
            "assistance": "Front squats, Bulgarian split squats, leg press"
        }
    }

    # Simple keyword matching (can use embeddings for better matching)
    if "bench" in user_query.lower():
        return knowledge_base["bench_press"]
    # etc...
```

## 2. 🔧 Fine-Tuning (Advanced)

### Option A: Fine-tune Nemotron (If NVIDIA Allows)

**Create Training Dataset:**
```json
[
  {
    "input": "User stats: Bench 185x5, sleep 8hrs, soreness 2/10, goal: strength",
    "output": "Excellent recovery! You're primed for a PR attempt. Try 190x5 today. Your CNS is fresh with 8 hours sleep and minimal soreness. Use the first set to gauge bar speed - if it moves smoothly, you've got 195x3 in you. Focus on leg drive and staying tight.",
    "metadata": {"category": "strength_coaching", "experience": "intermediate"}
  },
  {
    "input": "User stats: Squat 225x5, sleep 5hrs, soreness 8/10, goal: muscle",
    "output": "Red flag on recovery. Your body needs rest more than stimulus right now. Drop to 185x8 today focusing on tempo (3 second descent). High soreness + poor sleep = injury risk. Prioritize protein (180g+) and get 8+ hours sleep tonight. Tomorrow you'll be ready to push.",
    "metadata": {"category": "recovery_management", "experience": "intermediate"}
  }
]
```

**Fine-tuning Code (Conceptual):**
```python
from nvidia_nim import FineTuning

# Load base model
model = FineTuning.load_model("nemotron-nano-12b-v2-vl")

# Prepare dataset
training_data = load_json("training_data.json")

# Fine-tune
model.fine_tune(
    data=training_data,
    epochs=3,
    learning_rate=2e-5,
    validation_split=0.1
)

# Save fine-tuned model
model.save("focusflow-nemotron-ft")
```

### Option B: Use Adapters (LoRA - Low Rank Adaptation)

Faster and cheaper than full fine-tuning:

```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM"
)

# Apply LoRA to model
model = get_peft_model(base_model, lora_config)

# Train only the adapter weights (much faster!)
trainer.train(model, training_data)
```

## 3. 📊 Collect User Data for Training

### Build a Feedback Loop:

**A. Rating System**
```python
def collect_feedback(recommendation, user_rating):
    """Store user ratings of AI recommendations"""
    feedback_entry = {
        "timestamp": datetime.now(),
        "user_data": user_stats,
        "recommendation": recommendation,
        "rating": user_rating,  # 1-5 stars
        "followed_advice": True/False,
        "outcome": "PR achieved" / "felt too hard" / etc.
    }

    # Store in database
    save_to_training_db(feedback_entry)
```

**B. A/B Testing**
```python
def ab_test_recommendations():
    """Test different coaching styles"""
    if user_id % 2 == 0:
        style = "aggressive"  # "Push harder! Add 10lbs!"
    else:
        style = "conservative"  # "Add 2.5lbs when ready"

    track_which_style_gets_better_results()
```

**C. Outcome Tracking**
```python
# Track if users actually PR after following advice
if recommendation == "Try 225lbs bench today":
    # 1 week later, check:
    if user.achieved_pr("bench", 225):
        positive_example = True  # Good recommendation
    else:
        negative_example = True  # Recalibrate
```

## 4. 🧠 Create a Knowledge Base

### Build Custom Fitness Database:

```python
# knowledge_base/exercises.json
{
  "bench_press": {
    "muscle_groups": ["chest", "triceps", "shoulders"],
    "difficulty": "intermediate",
    "form_cues": [
      "Retract scapula",
      "Arch lower back",
      "Feet flat on floor",
      "Bar path straight down to mid-chest"
    ],
    "common_mistakes": [
      "Bouncing bar off chest",
      "Flaring elbows too wide",
      "Not using leg drive"
    ],
    "progression_schemes": {
      "linear": "Add 2.5lbs every session when you hit target reps",
      "5/3/1": "Wave loading over 4 week blocks",
      "texas_method": "Volume day, light day, intensity day"
    },
    "deload_protocol": "Drop to 60% of working weight for 1 week every 4-6 weeks"
  }
}

# Use in prompts:
def get_exercise_info(exercise_name):
    knowledge = load_json("knowledge_base/exercises.json")
    info = knowledge.get(exercise_name, {})

    return f"""
EXERCISE: {exercise_name.upper()}
Muscles: {info['muscle_groups']}
Form: {', '.join(info['form_cues'])}
Progression: {info['progression_schemes']['linear']}
"""
```

## 5. 🔬 Model Evaluation & Testing

### Track Model Performance:

```python
def evaluate_recommendations():
    """Test model against known good recommendations"""

    test_cases = [
        {
            "input": "Bench 185x5, sleep 8hrs, soreness 2/10",
            "expected": "should recommend increasing weight",
            "actual": model_response,
            "score": similarity_score(expected, actual)
        }
    ]

    avg_score = sum(case['score'] for case in test_cases) / len(test_cases)
    print(f"Model accuracy: {avg_score}%")
```

### Create Test Suite:

```python
# tests/coaching_tests.py

def test_progressive_overload():
    """Model should recommend weight increase when recovery is good"""
    user_data = {
        "recent_lifts": {"bench": 185},
        "sleep_hours": 8,
        "soreness": 2,
        "completed_reps": 5  # Hit target
    }

    response = planner_agent.plan(user_data)

    assert "190" in response or "increase" in response.lower()
    assert "185" not in response  # Shouldn't keep same weight

def test_deload_recommendation():
    """Model should recommend rest when overtrained"""
    user_data = {
        "sleep_hours": 5,
        "soreness": 9,
        "energy": "low"
    }

    response = coach_agent.motivate(user_data)

    assert "rest" in response.lower() or "recovery" in response.lower()
    assert "PR" not in response  # Shouldn't push for PRs
```

## 6. 🎨 Specialize Models for Different Roles

### Train Different Models for Each Agent:

**Insight Agent → Analytical Model**
- Fine-tune on data analysis tasks
- Focus on pattern recognition
- Medical/scientific language

**Planner Agent → Strategic Model**
- Fine-tune on program design
- Periodization knowledge
- Exercise selection logic

**Coach Agent → Motivational Model**
- Fine-tune on motivational language
- Hype and encouragement
- Tough love when needed

## 7. 📈 Continuous Improvement Pipeline

### Automated Learning Loop:

```python
class ContinuousLearning:
    def __init__(self):
        self.feedback_db = FeedbackDatabase()
        self.model = load_model()

    def daily_training_cycle(self):
        """Run every 24 hours"""

        # 1. Collect yesterday's feedback
        feedback = self.feedback_db.get_last_24h()

        # 2. Filter high-quality examples (5-star ratings)
        good_examples = [f for f in feedback if f.rating >= 4]

        # 3. Convert to training format
        training_data = self.format_for_training(good_examples)

        # 4. Fine-tune model on new data
        self.model.fine_tune(training_data, epochs=1)

        # 5. Test on validation set
        accuracy = self.evaluate_model()

        # 6. Deploy if improved
        if accuracy > self.current_accuracy:
            self.deploy_model()

        return f"Model updated. Accuracy: {accuracy}%"
```

## 8. 🚀 Quick Wins (Implement Today)

### A. Add Exercise Encyclopedia to Prompts

```python
# In agents/planner.py
EXERCISE_DB = """
BENCH PRESS: Chest, triceps, shoulders. Start with bar path down to nipples. Add 2.5lbs every session.
SQUAT: Quads, glutes, core. Depth below parallel. Add 5lbs every session.
DEADLIFT: Full body. Start with conventional. Add 5-10lbs every session.
OVERHEAD PRESS: Shoulders, triceps. Most sensitive to fatigue. Add 2.5lbs or fractional plates.
"""

prompt = f"""
{EXERCISE_DB}

Based on this knowledge, create a workout plan...
"""
```

### B. Add Personalization Context

```python
user_profile = {
    "training_age": "2 years",
    "injury_history": ["lower back tweak 6 months ago"],
    "preferences": ["loves compound lifts", "hates cardio"],
    "schedule": "4 days/week",
    "equipment": "full gym access"
}

# Include in every prompt
context = f"""
USER PROFILE:
Experience: {user_profile['training_age']}
Injuries: {', '.join(user_profile['injury_history'])}
Preferences: {', '.join(user_profile['preferences'])}
"""
```

### C. Temperature Tuning

```python
# Different temperatures for different agents:

# Insight Agent: Lower temperature (more factual)
"temperature": 0.3  # Conservative, data-driven

# Planner Agent: Medium temperature (balanced)
"temperature": 0.6  # Some creativity in exercise selection

# Coach Agent: Higher temperature (more creative)
"temperature": 0.9  # Varied motivational language
```

## 9. 💾 Dataset Sources

Where to get training data:

**A. Reddit Scraping**
- r/Fitness
- r/weightroom
- r/bodybuilding
- Pull Q&A pairs from expert responses

**B. Fitness Coaching Books**
- Starting Strength (Mark Rippetoe)
- 5/3/1 (Jim Wendler)
- Renaissance Periodization
- Convert to Q&A format

**C. YouTube Transcripts**
- Jeff Nippard
- Renaissance Periodization
- Alan Thrall
- Extract coaching advice

**D. Create Synthetic Data**
```python
import random

def generate_training_example():
    bench = random.randint(135, 315)
    sleep = random.uniform(5, 9)
    soreness = random.randint(1, 10)

    # Rule-based ground truth
    if sleep > 7.5 and soreness < 4:
        advice = f"Great recovery! Try {bench + 5}lbs today."
    elif sleep < 6 or soreness > 7:
        advice = f"Recovery compromised. Drop to {bench - 10}lbs or rest."
    else:
        advice = f"Moderate recovery. Maintain {bench}lbs, focus on form."

    return {
        "input": f"Bench {bench}lbs, sleep {sleep}hrs, soreness {soreness}/10",
        "output": advice
    }

# Generate 10,000 examples
dataset = [generate_training_example() for _ in range(10000)]
```

## 10. 🎯 Evaluation Metrics

Track these to measure improvement:

```python
metrics = {
    "recommendation_accuracy": "% of times user agrees with advice",
    "pr_success_rate": "% of predicted PRs actually achieved",
    "injury_prevention": "# of times model prevented overtraining",
    "user_satisfaction": "Average rating of responses (1-5)",
    "adherence_rate": "% of users who follow the plan",
    "response_relevance": "Semantic similarity to expert responses"
}
```

## Summary: Best Approaches for Hackathon

**Immediate (Today):**
1. ✅ Add exercise knowledge base to prompts
2. ✅ Fine-tune temperature per agent
3. ✅ Add few-shot examples

**Short-term (This Week):**
1. Build feedback collection system
2. Create test suite for recommendations
3. Implement RAG with fitness knowledge base

**Long-term (After Hackathon):**
1. Collect real user data
2. Fine-tune with LoRA adapters
3. Continuous learning pipeline

The easiest and most impactful method for your hackathon is **prompt engineering + RAG** - no model retraining required!
