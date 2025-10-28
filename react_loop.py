#!/usr/bin/env python3
"""
Enhanced ReAct Loop - Multi-step agent reasoning with feedback cycles
Demonstrates: Reason → Act → Observe → Re-evaluate pattern
"""
import json
from agents.insight import analyze_user
from agents.planner import plan_next_day
from agents.coach import motivate_user
from notification_system import NotificationManager


class ReActLoop:
    """
    Multi-agent ReAct loop with feedback and re-evaluation
    Shows how agents can think in multiple steps and adjust based on feedback
    """

    def __init__(self, user_data):
        self.user_data = user_data
        self.iteration = 0
        self.max_iterations = 3
        self.feedback_history = []

    def reason(self):
        """Step 1: Insight Agent analyzes current state"""
        print(f"\n{'='*70}")
        print(f"🧠 STEP 1: REASON (Iteration {self.iteration + 1})")
        print(f"{'='*70}")

        # Add feedback history to context
        if self.feedback_history:
            self.user_data['feedback_history'] = self.feedback_history

        insight = analyze_user(self.user_data)
        print(insight)

        return insight

    def act(self, insight):
        """Step 2: Planner Agent creates action plan"""
        print(f"\n{'='*70}")
        print(f"📋 STEP 2: ACT")
        print(f"{'='*70}")

        plan = plan_next_day(insight, self.user_data)
        print(plan)

        return plan

    def observe(self, insight, plan):
        """Step 3: Coach Agent provides feedback and motivation"""
        print(f"\n{'='*70}")
        print(f"💪 STEP 3: OBSERVE & MOTIVATE")
        print(f"{'='*70}")

        coaching = motivate_user(insight, plan)
        print(coaching)

        return coaching

    def simulate_user_feedback(self, plan):
        """Step 4: Simulate user feedback on the plan"""
        print(f"\n{'='*70}")
        print(f"💬 STEP 4: USER FEEDBACK (Simulated)")
        print(f"{'='*70}")

        # Simulate different types of feedback based on user data
        feedback_scenarios = self._generate_feedback_scenarios()

        # Pick feedback based on recovery and iteration
        recovery_score = self._calculate_recovery()

        if self.iteration == 0:
            # First iteration: general feedback
            if recovery_score < 50:
                feedback = feedback_scenarios['too_hard']
            elif recovery_score > 85:
                feedback = feedback_scenarios['too_easy']
            else:
                feedback = feedback_scenarios['just_right']
        elif self.iteration == 1:
            # Second iteration: specific adjustments
            feedback = feedback_scenarios['adjust_volume']
        else:
            # Final iteration: confirmation
            feedback = feedback_scenarios['approved']

        print(f"User says: \"{feedback['message']}\"")
        print(f"Sentiment: {feedback['sentiment']}")
        print(f"Adjustment needed: {feedback['needs_adjustment']}")

        return feedback

    def re_evaluate(self, feedback):
        """Step 5: Re-evaluate and adjust based on feedback"""
        print(f"\n{'='*70}")
        print(f"🔄 STEP 5: RE-EVALUATE & ADJUST")
        print(f"{'='*70}")

        # Store feedback in history
        self.feedback_history.append({
            'iteration': self.iteration,
            'feedback': feedback['message'],
            'sentiment': feedback['sentiment']
        })

        # Adjust user data based on feedback
        if feedback['sentiment'] == 'negative':
            print("⚠️  Detected concerns. Adjusting plan difficulty...")
            # Reduce volume or intensity
            self.user_data['adjustment'] = 'reduce_volume'

        elif feedback['sentiment'] == 'positive' and feedback.get('too_easy'):
            print("💪 User ready for more! Increasing challenge...")
            # Increase volume or intensity
            self.user_data['adjustment'] = 'increase_intensity'

        else:
            print("✅ Plan approved! Moving forward...")
            return False  # Stop iterating

        return True  # Continue iterating

    def run(self):
        """Execute the full ReAct loop with feedback"""
        print("\n" + "="*70)
        print("🔄 STARTING ENHANCED ReAct LOOP")
        print("="*70)
        print("Demonstrating multi-step agent reasoning with feedback cycles")
        print()

        for i in range(self.max_iterations):
            self.iteration = i

            # Core ReAct cycle
            insight = self.reason()
            plan = self.act(insight)
            coaching = self.observe(insight, plan)

            # Feedback and re-evaluation
            feedback = self.simulate_user_feedback(plan)
            should_continue = self.re_evaluate(feedback)

            if not should_continue:
                print(f"\n✅ Plan finalized after {i + 1} iteration(s)")
                break

            if i < self.max_iterations - 1:
                print(f"\n🔄 Re-running with adjustments...")
                input("Press Enter to continue to next iteration...")

        # Generate notifications based on final plan
        print(f"\n{'='*70}")
        print("📲 GENERATING SMART NOTIFICATIONS")
        print(f"{'='*70}")

        notif_manager = NotificationManager(self.user_data)
        notifications = notif_manager.run_notification_check()

        print(f"\n{'='*70}")
        print("🎯 REACT LOOP COMPLETE")
        print(f"{'='*70}")
        print(f"Total iterations: {self.iteration + 1}")
        print(f"Feedback cycles: {len(self.feedback_history)}")
        print(f"Notifications generated: {len(notifications)}")

        return {
            'iterations': self.iteration + 1,
            'feedback_history': self.feedback_history,
            'final_plan': plan,
            'notifications': notifications
        }

    def _calculate_recovery(self):
        """Calculate recovery percentage"""
        sleep = self.user_data.get('sleep_hours', 7)
        soreness = self.user_data.get('soreness', 5)
        energy = self.user_data.get('energy', 'moderate')

        energy_scores = {'low': 60, 'moderate': 80, 'high': 100}

        sleep_score = min(sleep / 8 * 100, 100)
        soreness_score = (10 - soreness) * 10
        energy_score = energy_scores.get(energy, 80)

        return (sleep_score * 0.4 + soreness_score * 0.3 + energy_score * 0.3)

    def _generate_feedback_scenarios(self):
        """Generate different user feedback scenarios"""
        return {
            'too_hard': {
                'message': "This looks really intense. I'm not sure I can handle that volume with my current soreness.",
                'sentiment': 'negative',
                'needs_adjustment': True,
                'too_easy': False
            },
            'too_easy': {
                'message': "I feel great and recovered. Can we add more volume or intensity?",
                'sentiment': 'positive',
                'needs_adjustment': True,
                'too_easy': True
            },
            'just_right': {
                'message': "This looks challenging but doable. Maybe a bit more emphasis on my weak points?",
                'sentiment': 'neutral',
                'needs_adjustment': True,
                'too_easy': False
            },
            'adjust_volume': {
                'message': "I like the exercises, but can we adjust the sets/reps based on my energy?",
                'sentiment': 'neutral',
                'needs_adjustment': True,
                'too_easy': False
            },
            'approved': {
                'message': "Perfect! This is exactly what I need. Let's do this!",
                'sentiment': 'positive',
                'needs_adjustment': False,
                'too_easy': False
            }
        }


if __name__ == "__main__":
    # Test the enhanced ReAct loop
    from dotenv import load_dotenv
    load_dotenv()

    sample_data = {
        "user_id": "test_user",
        "date": "2025-01-20",
        "workout_done": True,
        "workout_type": "upper_body",
        "max_lifts": {
            "bench_press": 185,
            "squat": 225,
            "deadlift": 275,
            "overhead_press": 115
        },
        "recent_lifts": {
            "bench_press": 175,
            "overhead_press": 105
        },
        "protein_grams": 140,
        "calories": 2400,
        "sleep_hours": 6.5,
        "water_oz": 70,
        "soreness": 6,
        "energy": "moderate",
        "body_weight": 175
    }

    react_loop = ReActLoop(sample_data)
    results = react_loop.run()

    print("\n📊 SUMMARY:")
    print(f"   Completed in {results['iterations']} iteration(s)")
    print(f"   Feedback provided: {len(results['feedback_history'])} time(s)")
    print(f"   Notifications ready: {len(results['notifications'])}")
