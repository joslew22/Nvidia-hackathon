import streamlit as st
import datetime
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Import your agents
from agents.insight import analyze_user
from agents.coach import motivate_user
from agents.planner import plan_next_day

# Page config
st.set_page_config(
    page_title="💪 FitFlow - AI Gym Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern gym-style UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    .main-container {
        font-family: 'Inter', sans-serif;
    }

    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .workout-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
    }

    .agent-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    .agent-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .success-alert {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    .warning-alert {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    .input-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }

    .progress-ring {
        transform: rotate(-90deg);
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }

    .sidebar .stSelectbox > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state for the app"""
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': 'Fitness Warrior',
            'height': 175,
            'weight': 75,
            'age': 25,
            'experience': 'Intermediate',
            'goals': ['Build Muscle', 'Increase Strength']
        }

    if 'workout_history' not in st.session_state:
        st.session_state.workout_history = []

    if 'current_plan' not in st.session_state:
        st.session_state.current_plan = None

    if 'progress_data' not in st.session_state:
        st.session_state.progress_data = []

def main():
    initialize_session_state()

    # Hero section
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">💪 FitFlow AI Gym Coach</div>
        <div class="hero-subtitle">Your Personal AI-Powered Fitness Transformation System</div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🎯 Navigation")
        page = st.selectbox(
            "Choose Your Section:",
            ["🏠 Dashboard", "📊 Profile Setup", "🏋️ Workout Planner", "📈 Progress Tracker", "🎯 Goals & Analytics"],
            key="navigation"
        )

    # Route to different pages
    if page == "🏠 Dashboard":
        dashboard_page()
    elif page == "📊 Profile Setup":
        profile_setup_page()
    elif page == "🏋️ Workout Planner":
        workout_planner_page()
    elif page == "📈 Progress Tracker":
        progress_tracker_page()
    elif page == "🎯 Goals & Analytics":
        analytics_page()

def dashboard_page():
    """Main dashboard with quick overview"""
    st.markdown("## 🏠 Your Fitness Dashboard")

    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Workouts This Week</div>
            <div class="metric-value">4</div>
            <div class="metric-label">🔥 On Fire!</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Current Streak</div>
            <div class="metric-value">12</div>
            <div class="metric-label">Days Strong</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">PR This Month</div>
            <div class="metric-value">3</div>
            <div class="metric-label">New Records!</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Fitness Score</div>
            <div class="metric-value">87</div>
            <div class="metric-label">Elite Level</div>
        </div>
        """, unsafe_allow_html=True)

    # Quick action buttons
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏋️ Start Workout", use_container_width=True, type="primary"):
            st.session_state.navigation = "🏋️ Workout Planner"
            st.rerun()

    with col2:
        if st.button("📊 Log Progress", use_container_width=True):
            st.session_state.navigation = "📈 Progress Tracker"
            st.rerun()

    with col3:
        if st.button("🤖 Get AI Coach", use_container_width=True):
            generate_ai_coaching()

    # Today's motivation
    st.markdown("""
    <div class="success-alert">
        <h3>💪 Today's Motivation</h3>
        <p>"The pain you feel today will be the strength you feel tomorrow. Every rep counts, every set matters. You're not just building muscle - you're building an unstoppable mindset!"</p>
    </div>
    """, unsafe_allow_html=True)

def profile_setup_page():
    """Enhanced profile setup"""
    st.markdown("## 📊 Your Fitness Profile")

    with st.container():
        st.markdown('<div class="input-section">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 👤 Personal Info")
            name = st.text_input("Name", value=st.session_state.user_profile['name'])
            age = st.slider("Age", 16, 80, st.session_state.user_profile['age'])
            height = st.slider("Height (cm)", 140, 220, st.session_state.user_profile['height'])
            weight = st.slider("Weight (kg)", 40, 150, st.session_state.user_profile['weight'])

            # Calculate and display BMI
            bmi = weight / ((height/100) ** 2)
            bmi_status = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
            st.metric("BMI", f"{bmi:.1f}", bmi_status)

        with col2:
            st.markdown("### 🎯 Fitness Goals")
            experience = st.selectbox(
                "Experience Level",
                ["Beginner", "Intermediate", "Advanced"],
                index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.user_profile['experience'])
            )

            goals = st.multiselect(
                "Primary Goals",
                ["Build Muscle", "Lose Weight", "Increase Strength", "Improve Endurance", "Athletic Performance", "General Fitness"],
                default=st.session_state.user_profile['goals']
            )

            workout_days = st.multiselect(
                "Preferred Workout Days",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                default=["Monday", "Wednesday", "Friday"]
            )

            workout_time = st.time_input("Preferred Workout Time", datetime.time(18, 0))

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("💾 Save Profile", type="primary", use_container_width=True):
            st.session_state.user_profile.update({
                'name': name,
                'age': age,
                'height': height,
                'weight': weight,
                'experience': experience,
                'goals': goals,
                'workout_days': workout_days,
                'workout_time': str(workout_time)
            })
            st.success("Profile saved successfully! 🎉")

def workout_planner_page():
    """AI-powered workout planning"""
    st.markdown("## 🏋️ AI Workout Planner")

    # Current workout input
    st.markdown("### 📝 Today's Workout Data")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        workout_done = st.checkbox("✅ Completed workout today")
        workout_type = st.selectbox("Workout Type", ["Upper Body", "Lower Body", "Full Body", "Cardio", "Rest Day"])

        st.markdown("#### 💪 Current Max Lifts")
        bench_max = st.number_input("Bench Press (lbs)", min_value=0, value=185, step=5)
        squat_max = st.number_input("Squat (lbs)", min_value=0, value=225, step=5)
        deadlift_max = st.number_input("Deadlift (lbs)", min_value=0, value=275, step=5)
        ohp_max = st.number_input("Overhead Press (lbs)", min_value=0, value=115, step=5)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("#### 🍗 Nutrition & Recovery")
        protein = st.slider("Protein intake (g)", 0, 300, 80)
        calories = st.slider("Total calories", 1000, 4000, 1800)
        water = st.slider("Water intake (oz)", 0, 150, 40)

        sleep_hours = st.slider("Sleep last night (hours)", 4.0, 12.0, 7.5, 0.5)
        soreness = st.slider("Soreness level (1-10)", 1, 10, 5)
        energy = st.selectbox("Energy level", ["Low", "Moderate", "High"])
        st.markdown('</div>', unsafe_allow_html=True)

    # Generate AI plan button
    if st.button("🤖 Generate AI Workout Plan", type="primary", use_container_width=True):
        generate_ai_workout_plan({
            'workout_done': workout_done,
            'workout_type': workout_type.lower().replace(' ', '_'),
            'max_lifts': {
                'bench_press': bench_max,
                'squat': squat_max,
                'deadlift': deadlift_max,
                'overhead_press': ohp_max
            },
            'protein_grams': protein,
            'calories': calories,
            'water_oz': water,
            'sleep_hours': sleep_hours,
            'soreness': soreness,
            'energy': energy.lower(),
            'body_weight': st.session_state.user_profile['weight'] * 2.2  # Convert to lbs
        })

def generate_ai_workout_plan(user_data):
    """Generate workout plan using AI agents"""
    with st.container():
        # Progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Agent 1: Insight
        status_text.info("🧠 AI Insight Agent analyzing your fitness data...")
        progress_bar.progress(25)

        with st.spinner("Analyzing patterns..."):
            time.sleep(1)  # Simulate processing
            insights = analyze_user(user_data)

        # Agent 2: Planner
        status_text.info("📋 AI Planner Agent creating your personalized workout...")
        progress_bar.progress(50)

        with st.spinner("Designing workout plan..."):
            time.sleep(1)
            workout_plan = plan_next_day(insights, user_data)

        # Agent 3: Coach
        status_text.info("💪 AI Coach Agent generating motivation...")
        progress_bar.progress(75)

        with st.spinner("Preparing coaching..."):
            time.sleep(1)
            coaching = motivate_user(insights, workout_plan)

        progress_bar.progress(100)
        status_text.success("✅ AI Analysis Complete!")

        # Clear progress indicators
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()

        # Display results in beautiful cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="agent-section">
                <div class="agent-title">🧠 AI Insights</div>
                <div style="white-space: pre-wrap;">{insights}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="agent-section">
                <div class="agent-title">📋 Workout Plan</div>
                <div style="white-space: pre-wrap;">{workout_plan}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="agent-section">
                <div class="agent-title">💪 Coaching</div>
                <div style="white-space: pre-wrap;">{coaching}</div>
            </div>
            """, unsafe_allow_html=True)

        # Save to session state
        st.session_state.current_plan = {
            'date': datetime.date.today(),
            'insights': insights,
            'plan': workout_plan,
            'coaching': coaching,
            'user_data': user_data
        }

def generate_ai_coaching():
    """Quick AI coaching for dashboard"""
    sample_data = {
        'workout_done': True,
        'workout_type': 'upper_body',
        'max_lifts': {'bench_press': 185, 'squat': 225},
        'protein_grams': 120,
        'sleep_hours': 7.5,
        'energy': 'high'
    }

    with st.spinner("Getting your AI coach..."):
        insights = analyze_user(sample_data)
        coaching = motivate_user(insights, "Today's focus: Upper body strength")

    st.markdown(f"""
    <div class="success-alert">
        <h3>🤖 Your AI Coach Says:</h3>
        <p>{coaching[:200]}...</p>
    </div>
    """, unsafe_allow_html=True)

def progress_tracker_page():
    """Enhanced progress tracking"""
    st.markdown("## 📈 Progress Tracker")

    # Mock data for demonstration
    dates = pd.date_range(start='2024-01-01', end='2024-01-28', freq='D')
    progress_data = pd.DataFrame({
        'date': dates,
        'bench_press': [175 + i*0.5 + (i%7)*2 for i in range(len(dates))],
        'squat': [205 + i*0.7 + (i%5)*3 for i in range(len(dates))],
        'deadlift': [255 + i*0.8 + (i%6)*2 for i in range(len(dates))],
        'body_weight': [75 + (i%14)*0.2 for i in range(len(dates))],
        'workout_intensity': [6 + (i%3) + (i%7)*0.5 for i in range(len(dates))]
    })

    # Key metrics overview
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        current_bench = progress_data['bench_press'].iloc[-1]
        bench_improvement = current_bench - progress_data['bench_press'].iloc[0]
        st.metric("Bench Press", f"{current_bench:.0f} lbs", f"+{bench_improvement:.0f} lbs")

    with col2:
        current_squat = progress_data['squat'].iloc[-1]
        squat_improvement = current_squat - progress_data['squat'].iloc[0]
        st.metric("Squat", f"{current_squat:.0f} lbs", f"+{squat_improvement:.0f} lbs")

    with col3:
        current_deadlift = progress_data['deadlift'].iloc[-1]
        deadlift_improvement = current_deadlift - progress_data['deadlift'].iloc[0]
        st.metric("Deadlift", f"{current_deadlift:.0f} lbs", f"+{deadlift_improvement:.0f} lbs")

    with col4:
        avg_intensity = progress_data['workout_intensity'].mean()
        st.metric("Avg Intensity", f"{avg_intensity:.1f}/10", "🔥 Strong")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💪 Strength Progress")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=progress_data['date'], y=progress_data['bench_press'],
                                name='Bench Press', line=dict(color='#667eea', width=3)))
        fig.add_trace(go.Scatter(x=progress_data['date'], y=progress_data['squat'],
                                name='Squat', line=dict(color='#764ba2', width=3)))
        fig.add_trace(go.Scatter(x=progress_data['date'], y=progress_data['deadlift'],
                                name='Deadlift', line=dict(color='#f093fb', width=3)))

        fig.update_layout(
            title="Lift Progress Over Time",
            xaxis_title="Date",
            yaxis_title="Weight (lbs)",
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### ⚖️ Body Composition")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=progress_data['date'], y=progress_data['body_weight'],
                                name='Body Weight', fill='tonexty',
                                line=dict(color='#4facfe', width=3)))

        fig.update_layout(
            title="Body Weight Trend",
            xaxis_title="Date",
            yaxis_title="Weight (kg)",
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

def analytics_page():
    """Advanced analytics and goals"""
    st.markdown("## 🎯 Goals & Analytics")

    # Goal setting
    st.markdown("### 🎯 Set Your Goals")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Strength Goals")
        target_bench = st.number_input("Target Bench Press (lbs)", min_value=0, value=200)
        target_squat = st.number_input("Target Squat (lbs)", min_value=0, value=250)
        target_deadlift = st.number_input("Target Deadlift (lbs)", min_value=0, value=300)
        target_date = st.date_input("Target Date", datetime.date.today() + datetime.timedelta(days=90))

    with col2:
        st.markdown("#### Body Goals")
        target_weight = st.number_input("Target Weight (kg)", min_value=0.0, value=72.0, step=0.5)
        target_bf = st.slider("Target Body Fat %", 5, 30, 15)

        # Progress rings
        current_bench_progress = (185 / target_bench) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Bench Press Progress</div>
            <div class="metric-value">{current_bench_progress:.0f}%</div>
            <div class="metric-label">185/{target_bench} lbs</div>
        </div>
        """, unsafe_allow_html=True)

    # AI Recommendations
    st.markdown("### 🤖 AI Recommendations")

    recommendations = [
        "🎯 Focus on progressive overload - increase bench press by 2.5lbs next session",
        "💪 Your squat form is improving - ready for heavier weight",
        "🍗 Increase protein to 1.2g/lb bodyweight for optimal muscle growth",
        "😴 Aim for 8+ hours sleep for better recovery",
        "🏃 Add 1 cardio session for improved endurance"
    ]

    for rec in recommendations:
        st.markdown(f"""
        <div class="workout-card">
            <p style="margin: 0; font-size: 1.1rem;">{rec}</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()