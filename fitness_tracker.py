import streamlit as st
import datetime
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import your agents
from agents.insight import analyze_user
from agents.coach import motivate_user
from agents.planner import plan_next_day

# Page config
st.set_page_config(
    page_title="🏋️ FitFlow - AI Gym Coach",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #E53E3E;
        text-align: center;
        margin-bottom: 2rem;
    }
    .workout-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .progress-metric {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .notification-alert {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #f44336;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

def initialize_fitness_profile():
    """Initialize user fitness profile"""
    if 'fitness_profile' not in st.session_state:
        st.session_state.fitness_profile = {
            'height': 170,
            'weight': 70,
            'age': 25,
            'gender': 'Male',
            'fitness_level': 'Beginner',
            'goal': 'Build Muscle',
            'gym_schedule': ['Monday', 'Wednesday', 'Friday'],
            'preferred_time': '6:00 PM',
            'meal_times': ['8:00 AM', '1:00 PM', '7:00 PM']
        }

    if 'workout_history' not in st.session_state:
        st.session_state.workout_history = []

    if 'current_week_plan' not in st.session_state:
        st.session_state.current_week_plan = []

    if 'notifications' not in st.session_state:
        st.session_state.notifications = []

def main():
    initialize_fitness_profile()

    st.markdown('<h1 class="main-header">🏋️ FitFlow AI Gym Coach</h1>', unsafe_allow_html=True)
    st.markdown("**Personalized AI Fitness Coaching powered by NVIDIA NIM + Nemotron**")

    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "📋 Workout Plan", "📊 Progress", "🔔 Notifications"])

    with tab1:
        user_profile_page()

    with tab2:
        workout_plan_page()

    with tab3:
        progress_tracking_page()

    with tab4:
        notifications_page()

def user_profile_page():
    """User profile and fitness goals setup"""
    st.header("👤 Your Fitness Profile")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📏 Body Metrics")

        height = st.slider("Height (cm)", 140, 220, st.session_state.fitness_profile['height'])
        weight = st.slider("Weight (kg)", 40, 150, st.session_state.fitness_profile['weight'])
        age = st.slider("Age", 16, 80, st.session_state.fitness_profile['age'])
        gender = st.selectbox("Gender", ["Male", "Female", "Other"],
                             index=["Male", "Female", "Other"].index(st.session_state.fitness_profile['gender']))

        # Calculate BMI
        bmi = weight / ((height/100) ** 2)
        st.metric("BMI", f"{bmi:.1f}")

    with col2:
        st.subheader("🎯 Fitness Goals")

        fitness_level = st.selectbox(
            "Current Fitness Level",
            ["Beginner", "Intermediate", "Advanced"],
            index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.fitness_profile['fitness_level'])
        )

        goal = st.selectbox(
            "Primary Goal",
            ["Build Muscle", "Lose Weight", "Increase Strength", "General Fitness", "Athletic Performance"],
            index=["Build Muscle", "Lose Weight", "Increase Strength", "General Fitness", "Athletic Performance"].index(st.session_state.fitness_profile['goal'])
        )

        gym_days = st.multiselect(
            "Preferred Gym Days",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            default=st.session_state.fitness_profile['gym_schedule']
        )

        preferred_time = st.time_input("Preferred Workout Time",
                                     datetime.time(18, 0))

    st.subheader("🍽️ Meal Schedule")
    col1, col2, col3 = st.columns(3)
    with col1:
        breakfast = st.time_input("Breakfast", datetime.time(8, 0))
    with col2:
        lunch = st.time_input("Lunch", datetime.time(13, 0))
    with col3:
        dinner = st.time_input("Dinner", datetime.time(19, 0))

    if st.button("💾 Save Profile", type="primary", use_container_width=True):
        st.session_state.fitness_profile.update({
            'height': height,
            'weight': weight,
            'age': age,
            'gender': gender,
            'fitness_level': fitness_level,
            'goal': goal,
            'gym_schedule': gym_days,
            'preferred_time': str(preferred_time),
            'meal_times': [str(breakfast), str(lunch), str(dinner)]
        })
        st.success("Profile saved! 💪")

def workout_plan_page():
    """AI-generated workout plans"""
    st.header("📋 Your Personalized Workout Plan")

    if st.button("🤖 Generate New Weekly Plan", type="primary"):
        with st.spinner("AI agents creating your personalized workout plan..."):
            generate_workout_plan()

    if st.session_state.current_week_plan:
        display_workout_plan()
    else:
        st.info("Click 'Generate New Weekly Plan' to get your AI-powered workout routine!")

def generate_workout_plan():
    """Use AI agents to generate workout plan"""
    profile = st.session_state.fitness_profile

    # Create user data for insights
    user_data = {
        "height": profile['height'],
        "weight": profile['weight'],
        "age": profile['age'],
        "fitness_level": profile['fitness_level'],
        "goal": profile['goal'],
        "gym_days": len(profile['gym_schedule']),
        "experience": profile['fitness_level']
    }

    # Agent 1: Insight - Analyze fitness level and needs
    st.write("🧠 **Insight Agent**: Analyzing your fitness profile...")
    insight_prompt = f"""Analyze this user's fitness profile for workout planning:

Height: {profile['height']}cm
Weight: {profile['weight']}kg
Age: {profile['age']}
Fitness Level: {profile['fitness_level']}
Primary Goal: {profile['goal']}
Available Days: {len(profile['gym_schedule'])} days/week

Provide insights on:
1. Optimal training frequency and intensity
2. Muscle group priorities based on goal
3. Recommended progression strategy
4. Key areas to focus on"""

    insights = analyze_user(user_data)  # This will use your existing insight agent
    st.write(insights)

    # Agent 2: Planner - Create detailed workout plan
    st.write("📋 **Planner Agent**: Creating your workout routine...")
    plan_prompt = f"""Based on these insights, create a detailed weekly workout plan:

User Profile: {profile['fitness_level']} level, {profile['goal']}, {len(profile['gym_schedule'])} days/week
Available Days: {', '.join(profile['gym_schedule'])}

Insights: {insights}

Create a plan with:
1. Specific exercises for each day
2. Sets and reps for each exercise
3. Recommended weights (as % of body weight or difficulty level)
4. Rest periods between sets
5. Total workout duration

Format as a structured weekly plan."""

    workout_plan = plan_next_day(insights, user_data)
    st.write(workout_plan)

    # Agent 3: Coach - Motivational messages and tips
    st.write("💪 **Coach Agent**: Your personal motivation...")
    coaching = motivate_user(insights, workout_plan)
    st.write(coaching)

    # Save the generated plan
    st.session_state.current_week_plan = {
        'generated_date': datetime.date.today(),
        'insights': insights,
        'plan': workout_plan,
        'coaching': coaching,
        'profile_snapshot': profile.copy()
    }

def display_workout_plan():
    """Display the current workout plan"""
    plan = st.session_state.current_week_plan

    st.success(f"Plan generated on: {plan['generated_date']}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="workout-card">
            <h3>🧠 AI Insights</h3>
            <p>Analysis of your fitness profile</p>
        </div>
        """, unsafe_allow_html=True)
        st.write(plan['insights'])

    with col2:
        st.markdown("""
        <div class="workout-card">
            <h3>📋 Workout Plan</h3>
            <p>Your personalized routine</p>
        </div>
        """, unsafe_allow_html=True)
        st.write(plan['plan'])

    with col3:
        st.markdown("""
        <div class="workout-card">
            <h3>💪 Coaching</h3>
            <p>Motivation and tips</p>
        </div>
        """, unsafe_allow_html=True)
        st.write(plan['coaching'])

    # Workout logging
    st.subheader("✅ Log Today's Workout")
    col1, col2 = st.columns(2)

    with col1:
        completed_exercises = st.multiselect(
            "Completed Exercises",
            ["Push-ups", "Squats", "Deadlifts", "Bench Press", "Pull-ups", "Rows", "Cardio"]
        )

    with col2:
        workout_rating = st.slider("Workout Intensity (1-10)", 1, 10, 7)
        workout_duration = st.slider("Duration (minutes)", 15, 120, 60)

    if st.button("📝 Log Workout"):
        workout_entry = {
            'date': datetime.date.today(),
            'exercises': completed_exercises,
            'rating': workout_rating,
            'duration': workout_duration
        }
        st.session_state.workout_history.append(workout_entry)
        st.success("Workout logged! Great job! 🎉")

def progress_tracking_page():
    """Progress tracking and analytics"""
    st.header("📊 Your Fitness Progress")

    if not st.session_state.workout_history:
        st.info("Start logging workouts to see your progress!")
        return

    df = pd.DataFrame(st.session_state.workout_history)
    df['date'] = pd.to_datetime(df['date'])

    col1, col2 = st.columns(2)

    with col1:
        # Workout frequency
        st.subheader("🗓️ Workout Frequency")
        workout_counts = df.groupby(df['date'].dt.date).size()
        fig = px.bar(x=workout_counts.index, y=workout_counts.values,
                     title="Workouts per Day")
        st.plotly_chart(fig, use_container_width=True)

        # Workout intensity
        st.subheader("⚡ Workout Intensity")
        fig = px.line(df, x='date', y='rating',
                     title="Workout Intensity Over Time")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Duration tracking
        st.subheader("⏱️ Workout Duration")
        fig = px.scatter(df, x='date', y='duration',
                        title="Workout Duration (minutes)")
        st.plotly_chart(fig, use_container_width=True)

        # Progress metrics
        st.subheader("📈 Progress Metrics")

        total_workouts = len(df)
        avg_intensity = df['rating'].mean()
        avg_duration = df['duration'].mean()

        st.markdown(f"""
        <div class="progress-metric">
            <h3>Total Workouts: {total_workouts}</h3>
            <p>Average Intensity: {avg_intensity:.1f}/10</p>
            <p>Average Duration: {avg_duration:.0f} minutes</p>
        </div>
        """, unsafe_allow_html=True)

def notifications_page():
    """Real-time notifications and reminders"""
    st.header("🔔 Smart Notifications")

    current_time = datetime.datetime.now()
    profile = st.session_state.fitness_profile

    # Generate real-time notifications
    notifications = []

    # Gym time reminder
    preferred_time = datetime.datetime.strptime(profile['preferred_time'], "%H:%M:%S").time()
    current_day = current_time.strftime("%A")

    if current_day in profile['gym_schedule']:
        time_diff = datetime.datetime.combine(datetime.date.today(), preferred_time) - current_time
        if 0 <= time_diff.seconds <= 3600:  # Within 1 hour
            notifications.append({
                "type": "gym",
                "message": f"🏋️ Gym time in {time_diff.seconds//60} minutes!",
                "action": "Get your gym gear ready and head out!"
            })

    # Meal reminders
    for i, meal_time in enumerate(profile['meal_times']):
        meal_names = ["Breakfast", "Lunch", "Dinner"]
        meal_datetime = datetime.datetime.strptime(meal_time, "%H:%M:%S").time()
        meal_diff = datetime.datetime.combine(datetime.date.today(), meal_datetime) - current_time

        if 0 <= meal_diff.seconds <= 1800:  # Within 30 minutes
            notifications.append({
                "type": "meal",
                "message": f"🍽️ {meal_names[i]} time in {meal_diff.seconds//60} minutes!",
                "action": "Time for a nutritious meal to fuel your fitness goals!"
            })

    # Motivational notifications
    if current_time.hour == 9:  # Morning motivation
        notifications.append({
            "type": "motivation",
            "message": "🌅 Good morning! Ready to crush your fitness goals today?",
            "action": "Start with a healthy breakfast and plan your workout!"
        })

    # Display notifications
    if notifications:
        for notif in notifications:
            st.markdown(f"""
            <div class="notification-alert">
                <h4>{notif["message"]}</h4>
                <p><strong>Action:</strong> {notif["action"]}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active notifications. You're on track! 💪")

    # Manual notification settings
    st.subheader("⚙️ Notification Preferences")

    col1, col2 = st.columns(2)

    with col1:
        enable_gym_reminders = st.checkbox("🏋️ Gym Reminders", value=True)
        enable_meal_reminders = st.checkbox("🍽️ Meal Reminders", value=True)

    with col2:
        enable_motivation = st.checkbox("💪 Daily Motivation", value=True)
        enable_progress = st.checkbox("📊 Weekly Progress Reports", value=True)

    if st.button("💾 Save Notification Settings"):
        st.success("Notification preferences saved!")

if __name__ == "__main__":
    main()