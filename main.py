#!/usr/bin/env python3
"""
FocusFlow - AI Fitness Coaching System
Multi-agent system using NVIDIA NIM + Nemotron to optimize workouts,
track progressive overload, and maximize gains through Reason → Act → Observe loops
"""
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import agents
from agents.insight import analyze_user
from agents.coach import motivate_user
from agents.planner import plan_next_day


def load_user_data(filepath):
    """Load user data from JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found - {filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in {filepath}")
        sys.exit(1)


def display_report(data, insight, plan, coaching):
    """Display the FocusFlow fitness report"""
    print("\n" + "="*70)
    print("  💪 FOCUSFLOW FITNESS COACHING REPORT")
    print("="*70)

    print("\n📊 CURRENT STATS")
    print(f"   Date: {data.get('date', 'Unknown')}")
    print(f"   Body Weight: {data.get('body_weight', '?')} lbs")
    print(f"   Workout: {'✅ ' + data.get('workout_type', 'completed') if data.get('workout_done') else '❌ Rest Day'}")

    # Display max lifts
    max_lifts = data.get('max_lifts', {})
    if max_lifts:
        print(f"\n   💯 MAX LIFTS:")
        for lift, weight in max_lifts.items():
            print(f"      {lift.replace('_', ' ').title()}: {weight} lbs")

    # Display recent workout
    recent_lifts = data.get('recent_lifts', {})
    if recent_lifts:
        print(f"\n   🏋️  TODAY'S LIFTS:")
        for lift, weight in recent_lifts.items():
            print(f"      {lift.replace('_', ' ').title()}: {weight} lbs")

    print(f"\n   🍗 Nutrition:")
    print(f"      Protein: {data.get('protein_grams', '?')}g")
    print(f"      Calories: {data.get('calories', '?')}")
    print(f"      Water: {data.get('water_oz', '?')} oz")

    print(f"\n   😴 Recovery:")
    print(f"      Sleep: {data.get('sleep_hours', '?')} hours")
    print(f"      Soreness: {data.get('soreness', '?')}/10")
    print(f"      Energy: {data.get('energy', 'unknown').title()}")

    print("\n" + "-"*70)
    print("🧠 PERFORMANCE ANALYSIS (Reason)")
    print("-"*70)
    print(insight)

    print("\n" + "-"*70)
    print("📋 TOMORROW'S WORKOUT & MEAL PLAN (Act)")
    print("-"*70)
    print(plan)

    print("\n" + "-"*70)
    print("🔥 COACH'S MOTIVATION (Observe & Inspire)")
    print("-"*70)
    print(coaching)

    print("\n" + "="*70)
    print()


def interactive_mode():
    """Run FocusFlow in interactive CLI mode"""
    print("\n💪 FocusFlow Fitness Coach - Interactive Mode")
    print("="*70)

    # Collect user input
    try:
        workout_done = input("🏋️  Did you workout today? (y/n) ").lower().startswith('y')
        workout_type = input("   What type? (upper/lower/full/cardio/rest): ").lower() if workout_done else "rest"

        print("\n📊 Enter your max lifts (press Enter to skip):")
        bench = input("   Bench Press max (lbs): ")
        squat = input("   Squat max (lbs): ")
        deadlift = input("   Deadlift max (lbs): ")
        ohp = input("   Overhead Press max (lbs): ")

        max_lifts = {}
        if bench: max_lifts["bench_press"] = int(bench)
        if squat: max_lifts["squat"] = int(squat)
        if deadlift: max_lifts["deadlift"] = int(deadlift)
        if ohp: max_lifts["overhead_press"] = int(ohp)

        print("\n🍗 Nutrition:")
        protein = int(input("   Protein consumed today (grams): "))
        calories = int(input("   Total calories: "))
        water_oz = int(input("   Water intake (oz): "))

        print("\n😴 Recovery:")
        sleep_hours = float(input("   Sleep last night (hours): "))
        soreness = int(input("   Soreness level (1-10): "))
        energy = input("   Energy level (low/moderate/high): ").lower()

        body_weight = int(input("\n⚖️  Current body weight (lbs): "))

    except (ValueError, KeyboardInterrupt):
        print("\n❌ Invalid input or cancelled.")
        return

    # Create user data
    user_data = {
        "user_id": "interactive_user",
        "date": "today",
        "workout_done": workout_done,
        "workout_type": workout_type,
        "max_lifts": max_lifts,
        "recent_lifts": {},
        "protein_grams": protein,
        "calories": calories,
        "water_oz": water_oz,
        "sleep_hours": sleep_hours,
        "soreness": soreness,
        "energy": energy,
        "body_weight": body_weight
    }

    # Run agent pipeline
    print("\n🔄 Running AI coaching analysis...")
    run_pipeline(user_data)


def run_pipeline(data):
    """
    Execute the multi-agent ReAct loop:
    Reason (Insight) → Act (Plan) → Observe (Coach)
    """
    print("   → Insight Agent analyzing data...")
    insight = analyze_user(data)

    print("   → Planner Agent creating action plan...")
    plan = plan_next_day(insight, data)

    print("   → Coach Agent providing motivation...")
    coaching = motivate_user(insight, plan)

    # Display results
    display_report(data, insight, plan, coaching)


def main():
    """Main entry point"""
    # Check if API key is set
    if not os.getenv("NIM_API_KEY"):
        print("\n⚠️  WARNING: NIM_API_KEY not found!")
        print("   Set your NVIDIA NIM API key in the .env file")
        print("   Example: NIM_API_KEY=your_api_key_here\n")

    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive" or sys.argv[1] == "-i":
            interactive_mode()
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("\nFocusFlow - AI Wellness Agent System")
            print("\nUsage:")
            print("  python main.py [options] [data_file]")
            print("\nOptions:")
            print("  -i, --interactive    Run in interactive CLI mode")
            print("  -h, --help          Show this help message")
            print("\nExamples:")
            print("  python main.py data/sample_user.json")
            print("  python main.py --interactive")
            print()
        else:
            # Load data from file
            data_file = sys.argv[1]
            data = load_user_data(data_file)
            run_pipeline(data)
    else:
        # Default: use sample data
        print("\n💡 Running with default sample data")
        print("   Use --help to see all options\n")
        data_file = "data/sample_user.json"

        if not Path(data_file).exists():
            print(f"❌ Default file not found: {data_file}")
            print("   Use: python main.py --interactive")
            sys.exit(1)

        data = load_user_data(data_file)
        run_pipeline(data)


if __name__ == "__main__":
    main()
