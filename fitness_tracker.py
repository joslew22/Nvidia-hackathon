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

    # Notification settings (persistent)
    if 'notifications_enabled' not in st.session_state:
        st.session_state.notifications_enabled = True

    if 'active_notifications' not in st.session_state:
        st.session_state.active_notifications = []

def main():
    initialize_fitness_profile()

    st.markdown('<h1 class="main-header">🏋️ FitFlow AI Gym Coach</h1>', unsafe_allow_html=True)
    st.markdown("**Personalized AI Fitness Coaching powered by NVIDIA NIM + Nemotron**")

    # Sidebar for notifications toggle
    with st.sidebar:
        st.subheader("⚙️ Settings")
        notifications_enabled = st.toggle(
            "🔔 Enable Notifications",
            value=st.session_state.notifications_enabled,
            help="Get smart alerts for workouts, meals, and PR attempts"
        )
        st.session_state.notifications_enabled = notifications_enabled

        if notifications_enabled:
            st.success("✅ Notifications Active")
            # Auto-generate notifications in background
            if st.button("🔄 Refresh Notifications"):
                from notification_system import NotificationManager
                user_data = {
                    'body_weight': st.session_state.fitness_profile.get('weight', 70) * 2.2,
                    'sleep_hours': 7.5,
                    'soreness': 5,
                    'energy': 'moderate',
                    'max_lifts': {'bench_press': 185, 'squat': 225, 'deadlift': 275}
                }
                notif_manager = NotificationManager(user_data)
                notif_manager.run_notification_check()
                st.session_state.active_notifications = notif_manager.notifications
                st.rerun()
        else:
            st.info("🔕 Notifications Disabled")

    # Navigation tabs (removed ReAct Loop)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 Profile", "📸 Photo Analysis", "📋 Workout Plan", "📊 Progress", "🔔 Notifications"])

    with tab1:
        user_profile_page()

    with tab2:
        photo_analysis_page()

    with tab3:
        workout_plan_page()

    with tab4:
        progress_tracking_page()

    with tab5:
        notifications_page()

def photo_analysis_page():
    """Body photo analysis using Vision AI"""
    st.header("📸 AI Physique Analysis")

    st.markdown("""
    Upload a body photo and let our AI vision model analyze your physique to create
    a personalized workout plan based on your current development.
    """)

    # Photo upload
    uploaded_file = st.file_uploader("Upload Body Photo", type=['jpg', 'jpeg', 'png'])

    col1, col2 = st.columns([1, 1])

    with col1:
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Your Photo", use_column_width=True)

            # Fitness goal selection
            goal = st.selectbox(
                "Primary Fitness Goal",
                ["Build Muscle", "Lose Fat", "Get Lean/Toned", "General Fitness"]
            )

            if st.button("🔍 Analyze Physique", type="primary", use_container_width=True):
                with st.spinner("AI analyzing your physique... This may take 10-15 seconds"):
                    import base64
                    from agents.vision_analyzer import analyze_physique

                    # Convert uploaded file to base64
                    bytes_data = uploaded_file.getvalue()
                    base64_image = base64.b64encode(bytes_data).decode()

                    # Analyze
                    analysis = analyze_physique(image_base64=base64_image, user_goals=goal.lower())

                    # Store in session state
                    st.session_state['physique_analysis'] = analysis
                    st.session_state['analysis_goal'] = goal
                    st.success("✅ Analysis complete!")

    with col2:
        if 'physique_analysis' in st.session_state:
            st.subheader("🧠 AI Analysis Results")
            st.markdown("""
            <div class="workout-card">
                <h4>Physique Assessment</h4>
            </div>
            """, unsafe_allow_html=True)

            st.write(st.session_state['physique_analysis'])

            # Option to create workout plan based on analysis
            if st.button("💪 Create Custom Workout Plan", type="primary"):
                with st.spinner("Creating personalized workout plan..."):
                    from agents.vision_analyzer import create_visual_workout_plan

                    user_data = {
                        'goal': st.session_state['analysis_goal'].lower(),
                        'days_per_week': 4,
                        'experience': 'intermediate',
                        'body_weight': st.session_state.fitness_profile.get('weight', 180) * 2.2  # kg to lbs
                    }

                    workout_plan = create_visual_workout_plan(
                        st.session_state['physique_analysis'],
                        user_data
                    )

                    st.session_state['vision_workout_plan'] = workout_plan
                    st.success("✅ Custom plan created!")

            if 'vision_workout_plan' in st.session_state:
                st.markdown("""
                <div class="workout-card">
                    <h4>Your Custom Workout Plan</h4>
                </div>
                """, unsafe_allow_html=True)
                st.write(st.session_state['vision_workout_plan'])
        else:
            st.info("👆 Upload a photo to get started with AI analysis")

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

    # Create proper user data format for agents
    user_data = {
        "user_id": "streamlit_user",
        "date": str(datetime.date.today()),
        "workout_done": False,
        "workout_type": "planning",
        "max_lifts": {
            "bench_press": 135,  # Default starting values
            "squat": 185,
            "deadlift": 225,
            "overhead_press": 95
        },
        "recent_lifts": {},
        "protein_grams": 120,
        "calories": 2200,
        "sleep_hours": 7,
        "water_oz": 70,
        "soreness": 3,
        "energy": "moderate",
        "body_weight": profile['weight'] * 2.2,  # Convert kg to lbs
        "height": profile['height'],
        "age": profile['age'],
        "fitness_level": profile['fitness_level'],
        "goal": profile['goal'],
        "gym_days": len(profile['gym_schedule'])
    }

    # Agent 1: Insight - Analyze fitness level and needs
    st.write("🧠 **Insight Agent**: Analyzing your fitness profile...")

    insights = analyze_user(user_data)
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
    """Real-time notifications and reminders using NotificationManager"""
    st.header("🔔 Smart Notifications")

    # Check if notifications are enabled
    if not st.session_state.notifications_enabled:
        st.warning("🔕 Notifications are currently disabled. Enable them in the sidebar to receive alerts.")
        return

    st.markdown("""
    AI-powered notifications for workouts, meals, PR attempts, and recovery alerts.
    Notifications are updated automatically based on your profile and activity.
    """)

    # Display active notifications from sidebar
    if st.session_state.active_notifications:
        st.subheader(f"📬 Active Notifications ({len(st.session_state.active_notifications)})")

        for notif in st.session_state.active_notifications:
            priority_colors = {
                'high': '#ff9a9e',
                'medium': '#a8edea',
                'low': '#fed6e3'
            }

            color = priority_colors.get(notif['priority'], '#e0e0e0')

            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {color} 0%, #fecfef 100%);
                padding: 1.5rem;
                border-radius: 10px;
                border-left: 5px solid #f44336;
                margin: 1rem 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                animation: slideIn 0.3s ease-out;
            ">
                <h4 style="margin: 0; color: #333;">{notif['title']}</h4>
                <p style="margin: 0.5rem 0; color: #555;">{notif['message']}</p>
                <p style="margin: 0; font-size: 0.9rem; color: #666;"><strong>Priority:</strong> {notif['priority'].upper()}</p>
                {f'<p style="margin: 0; font-size: 0.9rem; color: #666;"><strong>Action:</strong> {notif["action"].replace("_", " ").title()}</p>' if notif['action'] != 'none' else ''}
                <p style="margin-top: 0.5rem; font-size: 0.8rem; color: #999;">{notif['timestamp'][:19]}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🔕 No active notifications. Click 'Refresh Notifications' in the sidebar to generate alerts.")

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