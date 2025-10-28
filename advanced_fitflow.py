import streamlit as st
import datetime
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import numpy as np

# Import your agents
from agents.insight import analyze_user
from agents.coach import motivate_user
from agents.planner import plan_next_day

# Page config
st.set_page_config(
    page_title="💪 FitFlow Pro - AI Gym Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with animations and modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 2s infinite;
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #fff, #f0f8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        font-weight: 300;
        margin-bottom: 0;
    }

    .metric-dashboard {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: translateX(-100%);
        transition: transform 0.6s;
    }

    .metric-card:hover::before {
        transform: translateX(100%);
    }

    .metric-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }

    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }

    .metric-trend {
        font-size: 0.8rem;
        margin-top: 0.5rem;
        opacity: 0.8;
    }

    .agent-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }

    .agent-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
        position: relative;
    }

    .agent-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }

    .agent-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .agent-icon {
        font-size: 2rem;
        padding: 0.8rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
    }

    .agent-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2d3748;
    }

    .agent-content {
        color: #4a5568;
        line-height: 1.6;
        font-size: 0.95rem;
    }

    .progress-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
    }

    .input-group {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }

    .success-message {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    .warning-message {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    .quick-action-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }

    .chart-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    .goal-progress {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 10px;
        border-radius: 5px;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }

    .goal-progress::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: progress-shimmer 2s infinite;
    }

    @keyframes progress-shimmer {
        0% { width: 0%; }
        50% { width: 100%; }
        100% { width: 0%; }
    }

    .notification-popup {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.5s ease;
    }

    @keyframes slideIn {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }

    .sidebar .stSelectbox > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def initialize_advanced_state():
    """Initialize advanced session state"""
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': 'Fitness Warrior',
            'height': 175,
            'weight': 75,
            'age': 25,
            'experience': 'Intermediate',
            'goals': ['Build Muscle', 'Increase Strength'],
            'target_bench': 200,
            'target_squat': 250,
            'target_deadlift': 300
        }

    if 'workout_history' not in st.session_state:
        # Generate realistic workout history
        dates = pd.date_range(start='2024-01-01', end='2024-01-28', freq='D')
        st.session_state.workout_history = pd.DataFrame({
            'date': dates,
            'workout_done': [True if i % 2 == 0 else False for i in range(len(dates))],
            'bench_press': [175 + i*0.8 + np.random.normal(0, 2) for i in range(len(dates))],
            'squat': [205 + i*1.2 + np.random.normal(0, 3) for i in range(len(dates))],
            'deadlift': [255 + i*1.0 + np.random.normal(0, 2.5) for i in range(len(dates))],
            'body_weight': [75 + np.sin(i/7)*0.5 + np.random.normal(0, 0.2) for i in range(len(dates))],
            'workout_intensity': [6 + (i%3) + np.random.normal(0, 0.5) for i in range(len(dates))],
            'protein': [80 + i*0.5 + np.random.normal(0, 5) for i in range(len(dates))],
            'sleep': [7 + np.random.normal(0, 1) for i in range(len(dates))]
        })

    if 'notifications' not in st.session_state:
        st.session_state.notifications = []

    if 'current_workout' not in st.session_state:
        st.session_state.current_workout = None

def main():
    initialize_advanced_state()

    # Main header
    st.markdown("""
    <div class="main-header">
        <div class="hero-title">💪 FitFlow Pro</div>
        <div class="hero-subtitle">Advanced AI-Powered Fitness Transformation System</div>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced sidebar
    with st.sidebar:
        st.markdown("### 🚀 FitFlow Navigation")

        # Profile summary in sidebar
        profile = st.session_state.user_profile
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 1rem; border-radius: 10px; color: white; margin-bottom: 1rem;">
            <h4>👋 {profile['name']}</h4>
            <p>🎯 {', '.join(profile['goals'])}</p>
            <p>📊 {profile['experience']} Level</p>
        </div>
        """, unsafe_allow_html=True)

        page = st.selectbox(
            "Choose Section:",
            ["🏠 Dashboard", "🏋️ Workout Studio", "📊 Profile & Setup", "📈 Progress Analytics", "🎯 Goals & AI Coach", "🔄 Real-time Tracker"],
            key="main_nav"
        )

        # Quick stats in sidebar
        st.markdown("### ⚡ Quick Stats")
        recent_data = st.session_state.workout_history.iloc[-7:]  # Last 7 days
        workouts_this_week = recent_data['workout_done'].sum()
        avg_intensity = recent_data['workout_intensity'].mean()

        st.metric("This Week", f"{workouts_this_week} workouts")
        st.metric("Avg Intensity", f"{avg_intensity:.1f}/10")

    # Route to pages
    if page == "🏠 Dashboard":
        enhanced_dashboard()
    elif page == "🏋️ Workout Studio":
        workout_studio()
    elif page == "📊 Profile & Setup":
        profile_setup()
    elif page == "📈 Progress Analytics":
        progress_analytics()
    elif page == "🎯 Goals & AI Coach":
        goals_ai_coach()
    elif page == "🔄 Real-time Tracker":
        realtime_tracker()

def enhanced_dashboard():
    """Enhanced dashboard with real-time data"""
    st.markdown("## 🏠 Fitness Command Center")

    # Key metrics dashboard
    history = st.session_state.workout_history
    profile = st.session_state.user_profile

    col1, col2, col3, col4, col5 = st.columns(5)

    # Calculate metrics
    current_bench = history['bench_press'].iloc[-1]
    bench_progress = ((current_bench / profile['target_bench']) * 100)
    workouts_this_month = history['workout_done'].sum()
    current_streak = calculate_streak(history)
    fitness_score = calculate_fitness_score(history)
    pr_this_month = count_prs(history)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Current Streak</div>
            <div class="metric-value">{current_streak}</div>
            <div class="metric-trend">🔥 Days Strong</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">This Month</div>
            <div class="metric-value">{workouts_this_month}</div>
            <div class="metric-trend">💪 Workouts</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Bench Progress</div>
            <div class="metric-value">{bench_progress:.0f}%</div>
            <div class="metric-trend">🎯 To Goal</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Fitness Score</div>
            <div class="metric-value">{fitness_score}</div>
            <div class="metric-trend">📊 Elite Level</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">PRs This Month</div>
            <div class="metric-value">{pr_this_month}</div>
            <div class="metric-trend">🏆 New Records</div>
        </div>
        """, unsafe_allow_html=True)

    # Quick actions
    st.markdown("### ⚡ Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🏋️ Start Workout", use_container_width=True, type="primary"):
            st.session_state.main_nav = "🏋️ Workout Studio"
            st.rerun()

    with col2:
        if st.button("🤖 Get AI Coaching", use_container_width=True):
            get_quick_ai_coaching()

    with col3:
        if st.button("📊 Log Progress", use_container_width=True):
            show_quick_log_modal()

    with col4:
        if st.button("📈 View Analytics", use_container_width=True):
            st.session_state.main_nav = "📈 Progress Analytics"
            st.rerun()

    # Live charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 💪 Strength Progression (Last 30 Days)")

        fig = go.Figure()
        recent_data = history.tail(30)

        fig.add_trace(go.Scatter(
            x=recent_data['date'],
            y=recent_data['bench_press'],
            name='Bench Press',
            line=dict(color='#667eea', width=3),
            mode='lines+markers'
        ))

        fig.add_trace(go.Scatter(
            x=recent_data['date'],
            y=recent_data['squat'],
            name='Squat',
            line=dict(color='#764ba2', width=3),
            mode='lines+markers'
        ))

        fig.update_layout(
            height=300,
            template="plotly_white",
            showlegend=True,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 📊 Weekly Performance")

        # Create performance radar chart
        categories = ['Strength', 'Consistency', 'Recovery', 'Nutrition', 'Intensity']
        values = [85, 78, 92, 75, 88]  # Mock values

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(102, 126, 234, 0.3)',
            line=dict(color='#667eea', width=2),
            name='Performance'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            height=300,
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # AI insights section
    display_ai_insights()

def workout_studio():
    """Advanced workout planning studio"""
    st.markdown("## 🏋️ Workout Studio")

    tab1, tab2, tab3 = st.tabs(["🎯 Plan Workout", "📝 Log Session", "📋 Workout History"])

    with tab1:
        plan_workout_tab()

    with tab2:
        log_session_tab()

    with tab3:
        workout_history_tab()

def plan_workout_tab():
    """Workout planning interface"""
    st.markdown("### 🎯 AI Workout Planner")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        st.markdown("#### 📊 Current Status")

        workout_type = st.selectbox(
            "Today's Focus",
            ["Upper Body Power", "Lower Body Strength", "Full Body Circuit", "Cardio Endurance", "Recovery/Mobility"]
        )

        available_time = st.slider("Available Time (minutes)", 30, 120, 60, 5)
        energy_level = st.slider("Energy Level (1-10)", 1, 10, 7)
        equipment = st.multiselect(
            "Available Equipment",
            ["Barbell", "Dumbbells", "Resistance Bands", "Pull-up Bar", "Cardio Machine"],
            default=["Barbell", "Dumbbells"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Quick Stats")

        # Display current maxes
        profile = st.session_state.user_profile
        st.metric("Bench Max", f"{185} lbs")
        st.metric("Squat Max", f"{225} lbs")
        st.metric("Deadlift Max", f"{275} lbs")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🤖 Generate AI Workout Plan", type="primary", use_container_width=True):
        generate_advanced_workout_plan(workout_type, available_time, energy_level, equipment)

def generate_advanced_workout_plan(workout_type, time_available, energy, equipment):
    """Generate advanced AI workout plan"""

    # Create user data
    user_data = {
        'workout_type': workout_type.lower().replace(' ', '_'),
        'available_time': time_available,
        'energy_level': energy,
        'equipment': equipment,
        'max_lifts': {
            'bench_press': 185,
            'squat': 225,
            'deadlift': 275,
            'overhead_press': 115
        },
        'body_weight': st.session_state.user_profile['weight'] * 2.2,
        'workout_done': False,
        'sleep_hours': 7.5,
        'soreness': 3,
        'protein_grams': 120,
        'calories': 2200,
        'water_oz': 80
    }

    # Progress container
    progress_container = st.container()

    with progress_container:
        # Animated progress
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Step 1: Analysis
        with st.spinner("🧠 AI analyzing your fitness profile..."):
            status_text.info("🧠 Insight Agent analyzing your data...")
            for i in range(0, 35, 5):
                progress_bar.progress(i)
                time.sleep(0.1)

            insights = analyze_user(user_data)

        # Step 2: Planning
        with st.spinner("📋 Creating personalized workout plan..."):
            status_text.info("📋 Planner Agent designing your workout...")
            for i in range(35, 70, 5):
                progress_bar.progress(i)
                time.sleep(0.1)

            workout_plan = plan_next_day(insights, user_data)

        # Step 3: Coaching
        with st.spinner("💪 Generating motivational coaching..."):
            status_text.info("💪 Coach Agent preparing motivation...")
            for i in range(70, 100, 5):
                progress_bar.progress(i)
                time.sleep(0.1)

            coaching = motivate_user(insights, workout_plan)

        progress_bar.progress(100)
        status_text.success("✅ Your AI workout plan is ready!")

        time.sleep(1)
        progress_bar.empty()
        status_text.empty()

    # Display results in enhanced cards
    st.markdown('<div class="agent-container">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon">🧠</div>
                <div class="agent-title">AI Insights</div>
            </div>
            <div class="agent-content">{insights}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon">📋</div>
                <div class="agent-title">Workout Plan</div>
            </div>
            <div class="agent-content">{workout_plan}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-icon">💪</div>
                <div class="agent-title">Coaching</div>
            </div>
            <div class="agent-content">{coaching}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Save workout plan
    st.session_state.current_workout = {
        'date': datetime.date.today(),
        'type': workout_type,
        'insights': insights,
        'plan': workout_plan,
        'coaching': coaching,
        'time_allocated': time_available
    }

    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Save Plan", use_container_width=True):
            st.success("Workout plan saved! 🎉")

    with col2:
        if st.button("🏋️ Start Workout", use_container_width=True, type="primary"):
            st.info("Starting workout timer... Good luck! 💪")

    with col3:
        if st.button("📱 Share Plan", use_container_width=True):
            st.info("Plan copied to clipboard! 📋")

def log_session_tab():
    """Log workout session"""
    st.markdown("### 📝 Log Your Workout")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        st.markdown("#### 🏋️ Exercises Completed")

        exercises = st.multiselect(
            "Select exercises you did:",
            ["Bench Press", "Squat", "Deadlift", "Overhead Press", "Pull-ups", "Rows", "Dips", "Cardio"],
            default=["Bench Press", "Squat"]
        )

        # Dynamic input for each selected exercise
        exercise_data = {}
        for exercise in exercises:
            st.markdown(f"**{exercise}**")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                sets = st.number_input(f"Sets", min_value=1, max_value=10, value=3, key=f"{exercise}_sets")
            with col_b:
                reps = st.number_input(f"Reps", min_value=1, max_value=30, value=8, key=f"{exercise}_reps")
            with col_c:
                weight = st.number_input(f"Weight (lbs)", min_value=0, value=135, key=f"{exercise}_weight")

            exercise_data[exercise] = {'sets': sets, 'reps': reps, 'weight': weight}

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="input-group">', unsafe_allow_html=True)
        st.markdown("#### 📊 Session Metrics")

        duration = st.slider("Workout Duration (minutes)", 15, 180, 60)
        intensity = st.slider("Intensity (1-10)", 1, 10, 7)
        fatigue = st.slider("Post-Workout Fatigue (1-10)", 1, 10, 5)
        satisfaction = st.slider("Satisfaction (1-10)", 1, 10, 8)

        notes = st.text_area("Notes", placeholder="How did the workout feel? Any observations?")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("💾 Log Workout", type="primary", use_container_width=True):
        # Save workout data
        workout_log = {
            'date': datetime.date.today(),
            'exercises': exercise_data,
            'duration': duration,
            'intensity': intensity,
            'fatigue': fatigue,
            'satisfaction': satisfaction,
            'notes': notes
        }

        # Add to session state (in real app, save to database)
        if 'logged_workouts' not in st.session_state:
            st.session_state.logged_workouts = []
        st.session_state.logged_workouts.append(workout_log)

        st.markdown("""
        <div class="success-message">
            <h4>🎉 Workout Logged Successfully!</h4>
            <p>Great job completing your workout! Your progress has been recorded.</p>
        </div>
        """, unsafe_allow_html=True)

def workout_history_tab():
    """Display workout history"""
    st.markdown("### 📋 Workout History")

    if 'logged_workouts' in st.session_state and st.session_state.logged_workouts:
        for i, workout in enumerate(reversed(st.session_state.logged_workouts[-10:])):  # Show last 10
            with st.expander(f"🏋️ {workout['date']} - {workout['duration']} minutes"):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Exercises:**")
                    for exercise, data in workout['exercises'].items():
                        st.write(f"• {exercise}: {data['sets']}x{data['reps']} @ {data['weight']}lbs")

                with col2:
                    st.markdown("**Metrics:**")
                    st.write(f"• Intensity: {workout['intensity']}/10")
                    st.write(f"• Satisfaction: {workout['satisfaction']}/10")
                    st.write(f"• Fatigue: {workout['fatigue']}/10")

                if workout['notes']:
                    st.markdown(f"**Notes:** {workout['notes']}")
    else:
        st.info("No workouts logged yet. Start by logging your first workout!")

def get_quick_ai_coaching():
    """Quick AI coaching for dashboard"""
    sample_data = {
        'workout_done': True,
        'workout_type': 'upper_body',
        'max_lifts': {'bench_press': 185, 'squat': 225, 'deadlift': 275},
        'protein_grams': 120,
        'sleep_hours': 7.5,
        'energy': 'high',
        'body_weight': 165
    }

    with st.spinner("🤖 Your AI coach is analyzing..."):
        time.sleep(1)  # Simulate processing
        insights = analyze_user(sample_data)
        coaching = motivate_user(insights, "Focus on progressive overload today!")

    st.markdown(f"""
    <div class="success-message">
        <h4>🤖 Your AI Coach Says:</h4>
        <p>{coaching[:300]}...</p>
    </div>
    """, unsafe_allow_html=True)

def show_quick_log_modal():
    """Quick log modal"""
    st.markdown("""
    <div class="success-message">
        <h4>📊 Quick Log</h4>
        <p>Navigate to the Workout Studio → Log Session for detailed workout logging!</p>
    </div>
    """, unsafe_allow_html=True)

def display_ai_insights():
    """Display AI insights on dashboard"""
    st.markdown("### 🤖 AI Insights & Recommendations")

    insights = [
        {
            'type': 'success',
            'icon': '🎯',
            'title': 'Progressive Overload Ready',
            'message': 'Your bench press recovery indicators suggest you\'re ready for a 2.5lb increase next session.'
        },
        {
            'type': 'warning',
            'icon': '😴',
            'title': 'Sleep Optimization',
            'message': 'Consider increasing sleep by 30 minutes for optimal recovery and strength gains.'
        },
        {
            'type': 'success',
            'icon': '💪',
            'title': 'Consistency Streak',
            'message': 'Excellent workout consistency! You\'re building strong habits for long-term success.'
        }
    ]

    for insight in insights:
        if insight['type'] == 'success':
            st.markdown(f"""
            <div class="success-message">
                <h4>{insight['icon']} {insight['title']}</h4>
                <p>{insight['message']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="warning-message">
                <h4>{insight['icon']} {insight['title']}</h4>
                <p>{insight['message']}</p>
            </div>
            """, unsafe_allow_html=True)

def calculate_streak(history):
    """Calculate current workout streak"""
    streak = 0
    for i in range(len(history)-1, -1, -1):
        if history.iloc[i]['workout_done']:
            streak += 1
        else:
            break
    return streak

def calculate_fitness_score(history):
    """Calculate overall fitness score"""
    recent = history.tail(7)
    consistency = recent['workout_done'].mean() * 100
    avg_intensity = recent['workout_intensity'].mean() * 10
    sleep_quality = recent['sleep'].mean() * 12
    return int((consistency + avg_intensity + sleep_quality) / 3)

def count_prs(history):
    """Count personal records this month"""
    # Simplified - count days where lifts increased
    recent = history.tail(30)
    prs = 0
    for col in ['bench_press', 'squat', 'deadlift']:
        if len(recent) > 1:
            max_recent = recent[col].max()
            max_previous = history[col].iloc[:-30].max() if len(history) > 30 else 0
            if max_recent > max_previous:
                prs += 1
    return prs

def profile_setup():
    """Profile setup page - simplified for space"""
    st.markdown("## 📊 Profile & Setup")
    st.info("Profile setup interface would go here...")

def progress_analytics():
    """Progress analytics page - simplified for space"""
    st.markdown("## 📈 Progress Analytics")
    st.info("Detailed analytics interface would go here...")

def goals_ai_coach():
    """Goals and AI coach page - simplified for space"""
    st.markdown("## 🎯 Goals & AI Coach")
    st.info("Goals setting and AI coach interface would go here...")

def realtime_tracker():
    """Real-time tracker page - simplified for space"""
    st.markdown("## 🔄 Real-time Tracker")
    st.info("Real-time workout tracking interface would go here...")

if __name__ == "__main__":
    main()