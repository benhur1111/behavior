import pandas as pd
from sqlalchemy.orm import Session
from app.models.raw_event import RawEvent

def extract_raw_events(db: Session) -> pd.DataFrame:
    """Extract raw events from the database and return as a Pandas DataFrame."""
    events = db.query(RawEvent).all()
    if not events:
        return pd.DataFrame()
    
    data = []
    for event in events:
        data.append({
            "id": event.id,
            "timestamp": event.timestamp,
            "event_type": event.event_type,
            "user_id": event.user_id,
            "habit_id": event.habit_id,
            "metadata_json": event.metadata_json
        })
    
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df
