# 🚀 FocusFlow Hackathon Checklist

## Before the Hackathon (~10 min)

- [ ] Copy `.env.example` to `.env`
- [ ] Create Python virtual environment
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- [ ] Install dependencies
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Read through [README.md](README.md)
- [ ] Review agent code in `agents/` folder

## Day of Hackathon

### 1. Get API Key (First thing!)
- [ ] Get NVIDIA NIM API key from organizers
- [ ] Add to `.env` file: `NIM_API_KEY=your_key_here`

### 2. Verify API Connection (~5 min)
```bash
# Test individual agents
python agents/insight.py
python agents/coach.py
python agents/planner.py
```

**Expected**: Each should call the API and return responses

### 3. Test Full Pipeline (~5 min)
```bash
# Run with sample data
python main.py

# Try interactive mode
python main.py --interactive
```

### 4. Customize & Enhance (Pick 1-2)

#### Quick Wins (30-60 min each)
- [ ] Add Streamlit web UI
  ```bash
  pip install streamlit
  # Create streamlit_app.py
  ```
- [ ] Integrate external API (weather, quotes)
- [ ] Add data visualization with matplotlib
- [ ] Implement progress tracking (save history to JSON)

#### Advanced (1-2 hours)
- [ ] Deploy agents as separate NIM endpoints
- [ ] Add function calling for tool use
- [ ] Implement feedback loop (Coach critiques Plan)
- [ ] Create browser extension integration

### 5. Prepare Demo (~30 min)

- [ ] Create demo script (see README)
- [ ] Test with various input scenarios
- [ ] Prepare 2-3 sample user stories
- [ ] Screenshot or record video of output
- [ ] Write 1-paragraph project description

## Demo Talking Points

1. **Problem**: "97% of people struggle with doomscrolling - average 3+ hours/day"
2. **Solution**: "Multi-agent AI system that reasons about your habits"
3. **Tech**: "Three Nemotron agents using ReAct pattern: Reason → Act → Observe"
4. **Show**: Run live demo with interactive mode
5. **Impact**: "Personalized, actionable advice that adapts to each user"

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `NIM_API_KEY not found` | Add key to `.env` file |
| Module not found | Run `pip install -r requirements.txt` |
| API timeout | Check internet, verify API key |
| No output | Check API endpoint URL format |

## Quick Command Reference

```bash
# Activate virtual environment
source venv/bin/activate

# Run with default sample
python main.py

# Run with specific file
python main.py data/sample_user_good.json

# Interactive mode
python main.py --interactive

# Test individual agent
python agents/insight.py

# Install new package
pip install package_name
pip freeze > requirements.txt
```

## File Structure Reference

```
📁 Focus Flow/
├── 📄 main.py                  ← Run this
├── 📁 agents/
│   ├── insight.py             ← Agent 1: Analyze
│   ├── coach.py               ← Agent 2: Motivate
│   └── planner.py             ← Agent 3: Plan
├── 📁 data/
│   └── sample_user.json       ← Test data
├── 📄 requirements.txt        ← Dependencies
├── 📄 .env                    ← Your API key (create this!)
└── 📄 README.md               ← Full documentation
```

## Success Criteria

By end of hackathon, you should have:
- ✅ Working multi-agent pipeline
- ✅ Interactive CLI demo
- ✅ At least 1 enhancement (UI, API integration, etc.)
- ✅ Clear demonstration of ReAct pattern
- ✅ 2-minute demo presentation ready

---

**You've got this!** 🎯 The foundation is built - now add your creativity!
