from app.models.behavior import Behavior

def analyze_behavior(behavior: Behavior) -> str:
    if behavior.completed:
        return (
            f"Antigravity boost 🚀: "
            f"You completed '{behavior.name}'. "
            f"Consistency creates lift."
        )
    else:
        return (
            f"Antigravity counter-force ⚠️: "
            f"'{behavior.name}' was skipped. "
            f"What friction pulled you down today?"
        )
