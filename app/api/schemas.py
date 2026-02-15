from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class EventBase(BaseModel):
    event_type: str
    user_id: int
    habit_id: Optional[int] = None
    metadata_json: Optional[Dict[str, Any]] = None

class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class AntigravityRequest(BaseModel):
    objective: str
    observations: str

class AntigravityResponse(BaseModel):
    analysis: str
