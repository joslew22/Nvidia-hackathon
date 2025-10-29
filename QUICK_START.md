# FocusFlow - Quick Start Guide

## Prerequisites
- Python 3.10+
- NVIDIA NIM API key (set in `.env` file)
- Virtual environment activated

## Setup

### 1. Activate Virtual Environment
```bash
cd "/Users/danieladewale/Desktop/Focus Flow"
source venv/bin/activate
```

### 2. Verify API Key
Make sure your `.env` file contains:
```
NIM_API_KEY=nvapi-YOUR-KEY-HERE
```

**Important:** No spaces, no quotes around the value!

## Running the App

### Option 1: Streamlit Web Interface (Recommended)
```bash
streamlit run fitness_tracker.py
```

Then open your browser to: `http://localhost:8501`

**Features:**
- 📊 Dashboard with user profile
- 📝 Daily Check-in (log workouts, sleep, nutrition)
- 🎯 Workout Plan Generator
- 📸 Photo Analysis (upload body photos for AI assessment)
- 🔔 Smart Notifications (PR alerts, meal reminders, rest day suggestions)

### Option 2: Command Line Interface
```bash
python3 main.py
```

**Modes:**
- Single analysis (uses sample data)
- Interactive mode (answer questions for personalized plan)
- Batch mode (analyze multiple users from JSON files)

### Option 3: Test Individual Agents

**Insight Agent:**
```bash
python3 agents/insight.py
```

**Planner Agent:**
```bash
python3 agents/planner.py
```

**Coach Agent:**
```bash
python3 agents/coach.py
```

**Vision Analyzer:**
```bash
python3 test_vision.py "/path/to/body/photo.jpg"
```

## Common Issues

### Issue: "command not found: streamlit"
**Solution:** Activate virtual environment first
```bash
source venv/bin/activate
streamlit run fitness_tracker.py
```

### Issue: ".env file not found"
**Solution:** Check `.env` format (no spaces, no quotes)
```
# Wrong:
NIM_API_KEY = "nvapi-key"

# Correct:
NIM_API_KEY=nvapi-key
```

### Issue: "404 Not Found" from API
**Solution:** Verify you're using the correct model (already fixed!)
- Model: `nvidia/nemotron-nano-12b-v2-vl`
- Endpoint: `https://integrate.api.nvidia.com/v1`

### Issue: Image path with spaces
**Solution:** Use quotes around file paths
```bash
# Wrong:
python3 test_vision.py ~/Downloads/my photo.jpg

# Correct:
python3 test_vision.py "~/Downloads/my photo.jpg"
```

## Project Structure

```
Focus Flow/
├── agents/
│   ├── insight.py          # Analyzes fitness data, recovery
│   ├── planner.py          # Creates workout + meal plans
│   ├── coach.py            # Provides motivation, PR guidance
│   └── vision_analyzer.py  # Body photo analysis
├── data/
│   └── sample_user*.json   # Test data files
├── main.py                 # CLI orchestrator
├── fitness_tracker.py      # Streamlit web app
├── knowledge_base.py       # Fitness knowledge (RAG)
├── notification_system.py  # Smart notifications
├── react_loop.py          # Multi-agent reasoning
└── .env                    # API key (keep secret!)
```

## Testing the Fix

To verify everything is working:

```bash
# Test all agents
source venv/bin/activate
python3 -c "
from agents.insight import analyze_user
from agents.planner import plan_next_day
from agents.coach import motivate_user

test_data = {
    'workout_done': False,
    'max_lifts': {'bench_press': 185, 'squat': 225},
    'sleep_hours': 7,
    'soreness': 3
}

insights = analyze_user(test_data)
plan = plan_next_day(insights, test_data)
coaching = motivate_user(insights, plan)

print('✅ All agents working!' if all([insights, plan, coaching]) else '❌ Error')
"
```

## Hackathon Demo Flow

**Recommended 4-minute demo:**

1. **Intro (30s):** "FocusFlow: AI fitness coach using NVIDIA Nemotron VL"
2. **Photo Analysis (1m):** Upload body photo, show AI assessment
3. **Multi-Agent Reasoning (1.5m):** Generate workout plan, show all 3 agents working
4. **Smart Notifications (30s):** Show PR alerts, meal reminders
5. **Wrap-up (30s):** Emphasize vision AI + multi-agent collaboration

## Key Features to Highlight

✅ **Vision-Language Model** - Analyzes body photos for custom plans
✅ **Multi-Agent System** - Insight, Planner, Coach agents collaborate
✅ **Progressive Overload AI** - Scientific weight progression recommendations
✅ **Recovery-Based Training** - Adjusts intensity based on sleep/soreness
✅ **Knowledge Base (RAG)** - Expert fitness knowledge without training
✅ **Smart Notifications** - PR alerts when recovery is optimal

## Documentation

- `README.md` - Full project documentation
- `TRAINING_GUIDE.md` - How to improve AI responses
- `ENHANCEMENT_IDEAS.md` - Future features roadmap
- `FIXES_APPLIED.md` - Recent bug fixes

## Support

**GitHub Repository:**
https://github.com/joslew22/Nvidia-hackathon

**API Documentation:**
https://docs.api.nvidia.com

---

Last Updated: October 28, 2024
Status: ✅ All systems operational
Model: nvidia/nemotron-nano-12b-v2-vl
