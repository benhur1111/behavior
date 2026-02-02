from fastapi import APIRouter
from app.models.behavior import Behavior
from app.services.tracker import add_behavior, list_behaviors
from app.agents.antigravity import analyze_behavior

router = APIRouter(prefix="/behaviors", tags=["behaviors"])

@router.post("")
def track_behavior(behavior: Behavior):
    saved = add_behavior(behavior)
    insight = analyze_behavior(saved)
    return {"behavior": saved, "insight": insight}

@router.get("")
def get_behaviors():
    return list_behaviors()

