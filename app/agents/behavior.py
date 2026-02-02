# app/agents/behavior_agent.py

from collections import Counter

class BehaviorAgent:
    def analyze(self, behaviors: list):
        if not behaviors:
            return {"message": "No data yet"}

        completed = [b for b in behaviors if b["completed"]]

        streak = len(completed)

        if streak >= 3:
            return {
                "insight": f"{streak}-day streak detected",
                "suggestion": "Try increasing intensity slightly"
            }

        return {
            "insight": "Low consistency",
            "suggestion": "Reduce difficulty and stay consistent"
        }
