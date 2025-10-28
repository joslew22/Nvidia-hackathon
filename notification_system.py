"""
Push Notification System - Mock API for sending workout reminders and motivation
"""
import json
import datetime
from pathlib import Path


class NotificationManager:
    """Simulates a push notification system for fitness coaching"""

    def __init__(self, user_data):
        self.user_data = user_data
        self.notifications = []
        self.notification_log = Path("data/notifications.json")

    def generate_workout_reminders(self):
        """Generate workout reminder notifications"""
        current_time = datetime.datetime.now()
        workout_time = current_time.replace(hour=18, minute=0)  # Default 6 PM

        time_until_workout = (workout_time - current_time).seconds // 60

        if 0 < time_until_workout <= 60:
            self.send_notification(
                title="🏋️ Workout Time Approaching!",
                message=f"Your workout starts in {time_until_workout} minutes. Get ready to crush it!",
                priority="high",
                action="open_workout_plan"
            )

    def generate_meal_reminders(self):
        """Generate meal prep reminders"""
        meal_times = [
            ("Breakfast", 8, 0),
            ("Pre-Workout Snack", 17, 0),
            ("Post-Workout Meal", 19, 30),
            ("Dinner", 20, 0)
        ]

        current_time = datetime.datetime.now()

        for meal_name, hour, minute in meal_times:
            meal_time = current_time.replace(hour=hour, minute=minute)
            time_diff = (meal_time - current_time).seconds // 60

            if 0 < time_diff <= 30:
                protein_target = self.user_data.get('body_weight', 180) * 0.8
                self.send_notification(
                    title=f"🍗 {meal_name} Time",
                    message=f"Time for nutrition! Aim for {protein_target/4:.0f}g protein this meal.",
                    priority="medium",
                    action="view_meal_plan"
                )

    def generate_pr_alerts(self):
        """Alert when ready for PR attempts based on recovery"""
        recovery_score = self._calculate_recovery_score()

        if recovery_score >= 85:
            max_lifts = self.user_data.get('max_lifts', {})
            if max_lifts:
                heaviest_lift = max(max_lifts.items(), key=lambda x: x[1])
                lift_name = heaviest_lift[0].replace('_', ' ').title()
                current_max = heaviest_lift[1]
                suggested_attempt = current_max + 5

                self.send_notification(
                    title="💪 PR ALERT: You're Ready!",
                    message=f"Recovery at {recovery_score}%! Try {suggested_attempt}lbs on {lift_name} today!",
                    priority="high",
                    action="log_pr_attempt"
                )

    def generate_rest_day_alerts(self):
        """Alert when recovery is poor and rest is needed"""
        recovery_score = self._calculate_recovery_score()

        if recovery_score < 50:
            self.send_notification(
                title="😴 Recovery Alert: Rest Recommended",
                message=f"Recovery at {recovery_score}%. Consider active recovery or complete rest today.",
                priority="high",
                action="view_recovery_tips"
            )

    def generate_motivation_quotes(self):
        """Send motivational notifications"""
        quotes = [
            "The only bad workout is the one that didn't happen. Get after it!",
            "Progressive overload = progressive results. Add that extra 2.5lbs!",
            "Your future self is counting on the work you do today.",
            "Strength isn't given. It's earned, rep by rep.",
            "The pain you feel today will be the strength you feel tomorrow."
        ]

        import random
        quote = random.choice(quotes)

        self.send_notification(
            title="💪 Daily Motivation",
            message=quote,
            priority="low",
            action="none"
        )

    def generate_progress_milestones(self):
        """Celebrate milestones and progress"""
        # Check for workout streaks, weight milestones, etc.
        max_lifts = self.user_data.get('max_lifts', {})

        # Example: Celebrate 225 bench milestone
        if max_lifts.get('bench_press', 0) >= 225:
            self.send_notification(
                title="🎉 MILESTONE UNLOCKED: 225lb Bench!",
                message="You hit two plates! That's elite level strength. Keep pushing!",
                priority="high",
                action="share_achievement"
            )

    def send_notification(self, title, message, priority="medium", action="none"):
        """Simulate sending a push notification"""
        notification = {
            "timestamp": datetime.datetime.now().isoformat(),
            "title": title,
            "message": message,
            "priority": priority,
            "action": action,
            "read": False
        }

        self.notifications.append(notification)
        self._log_notification(notification)

        # Simulate push notification display
        print(f"\n📲 PUSH NOTIFICATION [{priority.upper()}]")
        print(f"   {title}")
        print(f"   {message}")
        if action != "none":
            print(f"   👆 Tap to: {action.replace('_', ' ').title()}")
        print()

        return notification

    def _calculate_recovery_score(self):
        """Calculate recovery score from 0-100"""
        sleep = self.user_data.get('sleep_hours', 7)
        soreness = self.user_data.get('soreness', 5)
        energy = self.user_data.get('energy', 'moderate')

        energy_scores = {'low': 60, 'moderate': 80, 'high': 100}

        sleep_score = min(sleep / 8 * 100, 100)
        soreness_score = (10 - soreness) * 10
        energy_score = energy_scores.get(energy, 80)

        return (sleep_score * 0.4 + soreness_score * 0.3 + energy_score * 0.3)

    def _log_notification(self, notification):
        """Log notification to file for persistence"""
        try:
            if self.notification_log.exists():
                with open(self.notification_log, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []

            logs.append(notification)

            with open(self.notification_log, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not log notification: {e}")

    def run_notification_check(self):
        """Run all notification checks"""
        print("\n🔔 Running Notification System...")
        print("="*60)

        self.generate_workout_reminders()
        self.generate_meal_reminders()
        self.generate_pr_alerts()
        self.generate_rest_day_alerts()
        self.generate_motivation_quotes()
        self.generate_progress_milestones()

        print(f"\n✅ {len(self.notifications)} notifications generated")
        return self.notifications


if __name__ == "__main__":
    # Test the notification system
    sample_user = {
        "body_weight": 180,
        "sleep_hours": 8,
        "soreness": 3,
        "energy": "high",
        "max_lifts": {
            "bench_press": 225,
            "squat": 315,
            "deadlift": 405
        }
    }

    notif_manager = NotificationManager(sample_user)
    notif_manager.run_notification_check()
