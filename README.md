# 🎯 FocusFlow

**AI Wellness Agent System** - Reduce doomscrolling and build healthy habits with multi-agent AI powered by NVIDIA NIM + Nemotron

## Overview

FocusFlow is a demonstration of multi-agent AI reasoning using the **ReAct pattern** (Reason → Act → Observe). Three specialized Nemotron-powered agents work together to:

1. **Insight Agent** - Analyzes user wellness data to identify patterns
2. **Planner Agent** - Creates actionable next-day plans
3. **Coach Agent** - Provides motivational feedback and realistic advice

## Architecture

```
User Data → Insight Agent (Reason) → Planner Agent (Act) → Coach Agent (Observe) → User
```

Each agent makes independent LLM calls to NVIDIA NIM with specialized system prompts, demonstrating how multiple AI agents can collaborate on a complex problem.

## Quick Start

### Prerequisites

- Python 3.10+ (you have 3.13.7 ✅)
- NVIDIA NIM API key (get from hackathon organizers)
- VS Code (recommended)

### Installation

```bash
# 1. Navigate to project directory
cd "/Users/danieladewale/Desktop/Focus Flow"

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your NIM_API_KEY
```

### Configuration

Edit [.env](.env) and add your API key:

```bash
NIM_API_KEY=your_actual_api_key_here
```

## Usage

### Run with Sample Data

```bash
python main.py
```

Uses [data/sample_user.json](data/sample_user.json) by default.

### Run with Custom Data File

```bash
python main.py data/sample_user_good.json
python main.py data/sample_user_moderate.json
```

### Interactive Mode

```bash
python main.py --interactive
```

Enter your own wellness data and get real-time AI insights!

### Test Individual Agents

```bash
# Test Insight Agent
python agents/insight.py

# Test Coach Agent
python agents/coach.py

# Test Planner Agent
python agents/planner.py
```

## Project Structure

```
focusflow/
├── main.py                    # Main orchestration script
├── agents/
│   ├── __init__.py
│   ├── insight.py            # Insight Agent (analyzes patterns)
│   ├── coach.py              # Coach Agent (motivational feedback)
│   └── planner.py            # Planner Agent (creates action plans)
├── data/
│   ├── sample_user.json      # Sample: poor wellness day
│   ├── sample_user_good.json # Sample: good wellness day
│   └── sample_user_moderate.json
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── .gitignore
└── README.md
```

## Sample Output

```
============================================================
  🎯 FOCUSFLOW WELLNESS REPORT
============================================================

📊 USER DATA
   Date: 2025-01-15
   Scroll Time: 90 minutes
   Exercise: ❌ Skipped
   Mood: Tired
   Sleep: 5.5 hours
   Water: 3 glasses
   Breaks: 1 times

------------------------------------------------------------
🧠 INSIGHTS (Reason)
------------------------------------------------------------
[AI-generated analysis of patterns and behaviors...]

------------------------------------------------------------
📋 ACTION PLAN (Act)
------------------------------------------------------------
[AI-generated specific, actionable plan for tomorrow...]

------------------------------------------------------------
💪 COACHING (Observe & Motivate)
------------------------------------------------------------
[AI-generated motivational feedback and encouragement...]
```

## Customization Ideas

### Enhance the Agents

1. **Add External Tool Calls** - Use Nemotron's function calling to fetch:
   - Weather data (suggest outdoor activities)
   - Motivational quotes API
   - Calendar events (plan around meetings)

2. **Improve ReAct Loop** - Add feedback cycles:
   - Let Coach Agent critique the Plan
   - Let Planner adjust based on Coach feedback

3. **Add Memory** - Store past interactions:
   - Track progress over time
   - Identify long-term patterns
   - Celebrate wins

### Build a Web Interface

**Option 1: Flask** (minimal)
```bash
pip install flask
# Create app.py with simple form + API endpoint
```

**Option 2: Streamlit** (fastest)
```bash
pip install streamlit
# Create streamlit_app.py with interactive widgets
```

### Deploy to NVIDIA NIM Endpoints

Each agent can become a persistent endpoint:

```python
# Deploy Insight Agent
nim deploy --agent insight --model nemotron

# Deploy Coach Agent
nim deploy --agent coach --model nemotron

# Deploy Planner Agent
nim deploy --agent planner --model nemotron
```

Then call them via separate API endpoints for true distributed multi-agent orchestration.

## Hackathon Tips

### Show Off These Features

1. **Multi-Agent Reasoning** - Three specialized agents collaborating
2. **ReAct Pattern** - Clear Reason → Act → Observe flow
3. **NVIDIA NIM Integration** - Nemotron model with custom system prompts
4. **Interactive Demo** - Live CLI that responds to user input
5. **Production-Ready Structure** - Modular, testable, extensible code

### Quick Wins

- Add a simple visualization (matplotlib charts of scroll time trends)
- Integrate a real API (weather, calendar, quotes)
- Deploy one agent as a NIM endpoint
- Add a Streamlit UI for non-technical demo

### Demo Script

1. **Show the problem**: "I scroll 90 minutes a day and feel tired"
2. **Run interactive mode**: Input bad wellness data
3. **Show agent outputs**: Point out Reason → Act → Observe
4. **Improve and re-run**: Input better data, show positive reinforcement
5. **Explain architecture**: Multi-agent collaboration, not monolithic AI

## API Reference

### NVIDIA NIM Endpoint (Template)

```bash
curl -X POST https://api.nvidia.com/v1/nim/invoke \
  -H "Authorization: Bearer $NIM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nemotron",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant"},
      {"role": "user", "content": "Hello"}
    ],
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

**Note**: Adjust endpoint and payload structure based on actual NVIDIA NIM API documentation provided at the hackathon.

## Troubleshooting

### API Key Issues

```
⚠️  NIM_API_KEY not found
```

**Fix**: Copy [.env.example](.env.example) to `.env` and add your key.

### Import Errors

```
ModuleNotFoundError: No module named 'requests'
```

**Fix**: Install dependencies
```bash
pip install -r requirements.txt
```

### API Timeout/Connection Errors

- Check your internet connection
- Verify API key is valid
- Confirm NVIDIA NIM endpoint URL is correct

## Resources

- [NVIDIA NIM Documentation](https://developer.nvidia.com/nim)
- [Nemotron Model Info](https://developer.nvidia.com/nemotron)
- [ReAct Pattern Paper](https://arxiv.org/abs/2210.03629)
- [LangChain Multi-Agent Examples](https://python.langchain.com/docs/use_cases/agent_teams)

## License

MIT - Free to use for hackathon and beyond!

## Credits

Built for [Hackathon Name] using:
- NVIDIA NIM
- Nemotron LLM
- Python 3.13
- VS Code + Claude CLI

---

**Ready to build?** Start with `python main.py --interactive` and see the magic happen! 🚀
