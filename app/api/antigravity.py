from fastapi import APIRouter, HTTPException, Depends
from app.api.schemas import AntigravityRequest, AntigravityResponse
from app.agents.antigravity import AntigravityAgent

router = APIRouter(prefix="/antigravity", tags=["antigravity"])

def get_agent():
    return AntigravityAgent()

@router.post("/analyze", response_model=AntigravityResponse)
async def analyze_behavior(
    request: AntigravityRequest,
    agent: AntigravityAgent = Depends(get_agent)
):
    try:
        analysis = agent.analyze(request.objective, request.observations)
        return AntigravityResponse(analysis=analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
