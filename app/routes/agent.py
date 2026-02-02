# app/routes/agent.py

from fastapi import APIRouter
from app.agents.behavior_agent import BehaviorAgent
from app.storage import behaviors

router = APIRouter()
agent = BehaviorAgent()

@router.get("/insights")
def get_insights():
    return agent.analyze(behaviors)
