from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemas import EventCreate, EventRead
from app.core.database import get_db
from app.models.raw_event import RawEvent
from typing import List

router = APIRouter(prefix="/events", tags=["events"])

@router.post("", response_model=EventRead, status_code=201)
def ingest_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = RawEvent(
        event_type=event.event_type,
        user_id=event.user_id,
        habit_id=event.habit_id,
        metadata_json=event.metadata_json
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.post("/batch", response_model=List[EventRead], status_code=201)
def ingest_events_batch(events: List[EventCreate], db: Session = Depends(get_db)):
    db_events = [
        RawEvent(
            event_type=e.event_type,
            user_id=e.user_id,
            habit_id=e.habit_id,
            metadata_json=e.metadata_json
        ) for e in events
    ]
    db.add_all(db_events)
    db.commit()
    for e in db_events:
        db.refresh(e)
    return db_events
