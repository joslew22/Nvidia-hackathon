import streamlit as st
import json
import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

# Import your agents
from agents.insight import analyze_user
from agents.coach import motivate_user
from agents.planner import plan_next_day

# Page config
st.set_page_config(
    page_title="🎯 FocusFlow - AI Wellness Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 FocusFlow AI Wellness Coach</h1>', unsafe_allow_html=True)
    st.markdown("**Multi-agent AI system powered by NVIDIA NIM + Nemotron**")
    st.markdown("---")

    # Sidebar for navigation
    with st.sidebar:
        st.title("🎯 Navigation")
        mode = st.radio(
            "Choose Mode:",
            ["📊 Daily Analysis", "📈 Progress Dashboard", "🔧 Settings"]
        )

    if mode == "📊 Daily Analysis":
        daily_analysis_page()
    elif mode == "📈 Progress Dashboard":
        progress_dashboard_page()
    elif mode == "🔧 Settings":
        settings_page()

def daily_analysis_page():
    st.header("📊 Daily Wellness Analysis")

    # Input section
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📱 Digital Wellness")
        scroll_minutes = st.slider(
            "Screen scrolling time (minutes)",
            0, 300, 45,
            help="How much time did you spend scrolling social media/news?"
        )
        screen_breaks = st.slider("Screen time breaks taken", 0, 10, 3)

        st.subheader("💪 Physical Wellness")
        gym_done = st.checkbox("Completed exercise/gym today")
        sleep_hours = st.slider("Hours of sleep", 4.0, 12.0, 7.5, 0.5)

    with col2:
        st.subheader("🧠 Mental Wellness")
        mood = st.selectbox(
            "Current mood",
            ["energized", "neutral", "tired", "stressed", "happy", "anxious"]
        )
        water_intake = st.slider("Glasses of water", 0, 15, 6)

        st.subheader("📅 Today's Date")
        date = st.date_input("Date", datetime.date.today())

    # Analysis button
    if st.button("🚀 Analyze My Day", type="primary", use_container_width=True):
        # Create user data
        user_data = {
            "user_id": "streamlit_user",
            "date": str(date),
            "scroll_minutes": scroll_minutes,
            "gym_done": gym_done,
            "mood": mood,
            "sleep_hours": sleep_hours,
            "water_intake": water_intake,
            "screen_time_breaks": screen_breaks
        }

        # Save to session state for progress tracking
        if 'user_history' not in st.session_state:
            st.session_state.user_history = []
        st.session_state.user_history.append(user_data)

        # Run the multi-agent analysis
        with st.spinner("🤖 AI agents are analyzing your day..."):
            analyze_and_display(user_data)

def analyze_and_display(user_data):
    """Run the multi-agent pipeline and display results"""

    # Progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Agent 1: Insight
    status_text.text("🧠 Insight Agent analyzing patterns...")
    progress_bar.progress(33)
    insight = analyze_user(user_data)

    # Agent 2: Planner
    status_text.text("📋 Planner Agent creating action plan...")
    progress_bar.progress(66)
    plan = plan_next_day(insight, user_data)

    # Agent 3: Coach
    status_text.text("💪 Coach Agent providing motivation...")
    progress_bar.progress(100)
    coaching = motivate_user(insight, plan)

    # Clear progress indicators
    progress_bar.empty()
    status_text.empty()

    # Display results in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="agent-section">', unsafe_allow_html=True)
        st.subheader("🧠 Insights (Reason)")
        st.write(insight)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="agent-section">', unsafe_allow_html=True)
        st.subheader("📋 Action Plan (Act)")
        st.write(plan)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="agent-section">', unsafe_allow_html=True)
        st.subheader("💪 Coaching (Observe)")
        st.write(coaching)
        st.markdown('</div>', unsafe_allow_html=True)

    # Wellness score calculation (simple example)
    wellness_score = calculate_wellness_score(user_data)

    st.markdown("---")
    st.subheader("📊 Your Wellness Score Today")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Score", f"{wellness_score}/100", f"{wellness_score-75:+d}")
    with col2:
        screen_score = max(0, 100 - user_data['scroll_minutes'])
        st.metric("Screen Health", f"{screen_score}/100")
    with col3:
        sleep_score = min(100, int(user_data['sleep_hours'] * 12.5))
        st.metric("Sleep Quality", f"{sleep_score}/100")
    with col4:
        activity_score = 100 if user_data['gym_done'] else 30
        st.metric("Activity Level", f"{activity_score}/100")

def progress_dashboard_page():
    st.header("📈 Progress Dashboard")

    if 'user_history' not in st.session_state or not st.session_state.user_history:
        st.info("No data yet! Complete a daily analysis first.")
        return

    # Convert history to DataFrame
    df = pd.DataFrame(st.session_state.user_history)
    df['date'] = pd.to_datetime(df['date'])
    df['wellness_score'] = df.apply(calculate_wellness_score, axis=1)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📱 Screen Time Trend")
        fig = px.line(df, x='date', y='scroll_minutes',
                     title="Daily Scroll Time (minutes)")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("😴 Sleep Pattern")
        fig = px.bar(df, x='date', y='sleep_hours',
                    title="Sleep Hours per Day")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📊 Wellness Score Over Time")
        fig = px.line(df, x='date', y='wellness_score',
                     title="Overall Wellness Score")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("💧 Hydration Tracking")
        fig = px.area(df, x='date', y='water_intake',
                     title="Daily Water Intake (glasses)")
        st.plotly_chart(fig, use_container_width=True)

def settings_page():
    st.header("🔧 Settings")

    st.subheader("🤖 AI Model Configuration")
    st.info("NVIDIA NIM API settings are configured in your .env file")

    st.subheader("📊 Data Management")
    if st.button("Clear History"):
        if 'user_history' in st.session_state:
            st.session_state.user_history = []
            st.success("History cleared!")

    if st.button("Export Data"):
        if 'user_history' in st.session_state:
            data_json = json.dumps(st.session_state.user_history, indent=2)
            st.download_button(
                "Download JSON",
                data_json,
                "focusflow_data.json",
                "application/json"
            )

def calculate_wellness_score(data):
    """Simple wellness score calculation"""
    score = 0

    # Screen time (0-30 points)
    scroll_score = max(0, 30 - (data['scroll_minutes'] // 3))
    score += scroll_score

    # Exercise (25 points)
    score += 25 if data['gym_done'] else 0

    # Sleep (0-25 points)
    sleep_hours = data['sleep_hours']
    sleep_score = min(25, max(0, (sleep_hours - 4) * 5))
    score += sleep_score

    # Water (0-10 points)
    water_score = min(10, data['water_intake'])
    score += water_score

    # Breaks (0-10 points)
    breaks_score = min(10, data['screen_time_breaks'] * 2)
    score += breaks_score

    return min(100, score)

if __name__ == "__main__":
    main()