#!/usr/bin/env python3
"""
FocusFlow - AI Wellness Agent System
Multi-agent system using NVIDIA NIM + Nemotron to reduce doomscrolling
and build healthy habits through Reason → Act → Observe loops
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
    """Display the FocusFlow report in a formatted way"""
    print("\n" + "="*60)
    print("  🎯 FOCUSFLOW WELLNESS REPORT")
    print("="*60)

    print("\n📊 USER DATA")
    print(f"   Date: {data.get('date', 'Unknown')}")
    print(f"   Scroll Time: {data.get('scroll_minutes', 0)} minutes")
    print(f"   Exercise: {'✅ Done' if data.get('gym_done') else '❌ Skipped'}")
    print(f"   Mood: {data.get('mood', 'unknown').capitalize()}")
    print(f"   Sleep: {data.get('sleep_hours', '?')} hours")
    print(f"   Water: {data.get('water_intake', '?')} glasses")
    print(f"   Breaks: {data.get('screen_time_breaks', 0)} times")

    print("\n" + "-"*60)
    print("🧠 INSIGHTS (Reason)")
    print("-"*60)
    print(insight)

    print("\n" + "-"*60)
    print("📋 ACTION PLAN (Act)")
    print("-"*60)
    print(plan)

    print("\n" + "-"*60)
    print("💪 COACHING (Observe & Motivate)")
    print("-"*60)
    print(coaching)

    print("\n" + "="*60)
    print()


def interactive_mode():
    """Run FocusFlow in interactive CLI mode"""
    print("\n🎯 FocusFlow Interactive Mode")
    print("="*60)

    # Collect user input
    try:
        scroll_mins = int(input("📱 How many minutes did you scroll today? "))
        gym_done = input("💪 Did you exercise today? (y/n) ").lower().startswith('y')
        mood = input("😊 How do you feel? (energized/tired/neutral/stressed) ").lower()
        sleep_hours = float(input("😴 How many hours did you sleep? "))
        water_intake = int(input("💧 How many glasses of water? "))
        breaks = int(input("⏸️  How many screen breaks did you take? "))
    except (ValueError, KeyboardInterrupt):
        print("\n❌ Invalid input or cancelled.")
        return

    # Create user data
    user_data = {
        "user_id": "interactive_user",
        "date": "today",
        "scroll_minutes": scroll_mins,
        "gym_done": gym_done,
        "mood": mood,
        "sleep_hours": sleep_hours,
        "water_intake": water_intake,
        "screen_time_breaks": breaks
    }

    # Run agent pipeline
    print("\n🔄 Running multi-agent analysis...")
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
