#!/usr/bin/env python3
"""
Test Vision Analysis Feature
Upload a body photo and get AI-powered physique analysis and workout recommendations
"""
import os
import sys
from dotenv import load_dotenv
from agents.vision_analyzer import analyze_physique, create_visual_workout_plan

load_dotenv()

def main():
    print("\n" + "="*70)
    print("  📸 FOCUSFLOW VISION ANALYSIS TEST")
    print("="*70)

    # Check API key
    if not os.getenv("NIM_API_KEY"):
        print("\n❌ Error: NIM_API_KEY not found in .env file")
        sys.exit(1)

    # Get image path
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input("\n📁 Enter path to your body photo: ").strip()

    # Check if file exists
    if not os.path.exists(image_path):
        print(f"\n❌ Error: Image not found at {image_path}")
        sys.exit(1)

    # Get fitness goal
    print("\nFitness Goals:")
    print("  1. Build Muscle")
    print("  2. Lose Fat")
    print("  3. Get Lean/Toned")
    print("  4. General Fitness")

    goal_choice = input("\nSelect your goal (1-4): ").strip()

    goals = {
        "1": "build muscle",
        "2": "lose fat",
        "3": "get lean and toned",
        "4": "general fitness"
    }

    fitness_goal = goals.get(goal_choice, "build muscle")

    print(f"\n🔄 Analyzing your physique for goal: {fitness_goal}...")
    print("   This may take 10-15 seconds...\n")

    # Analyze physique
    analysis = analyze_physique(image_path=image_path, user_goals=fitness_goal)

    print("="*70)
    print("📸 PHYSIQUE ANALYSIS")
    print("="*70)
    print(analysis)
    print("\n" + "="*70)

    # Ask if user wants workout plan
    create_plan = input("\n💪 Would you like a customized workout plan based on this analysis? (y/n) ").lower().startswith('y')

    if create_plan:
        print("\n🔄 Creating your personalized workout plan...")

        # Get additional info
        days_per_week = input("   How many days/week can you train? (3-6): ").strip()
        experience = input("   Experience level? (beginner/intermediate/advanced): ").lower().strip()
        body_weight = input("   Current body weight (lbs): ").strip()

        user_data = {
            "goal": fitness_goal,
            "days_per_week": int(days_per_week) if days_per_week.isdigit() else 4,
            "experience": experience if experience else "intermediate",
            "body_weight": int(body_weight) if body_weight.isdigit() else 180
        }

        workout_plan = create_visual_workout_plan(analysis, user_data)

        print("\n" + "="*70)
        print("🏋️  PERSONALIZED WORKOUT PLAN")
        print("="*70)
        print(workout_plan)
        print("\n" + "="*70)

    print("\n✅ Analysis complete! Use this info in your main FocusFlow app.")
    print("   Run: python3 main.py --interactive\n")


if __name__ == "__main__":
    main()
