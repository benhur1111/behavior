from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.habit import Habit

class RawEvent(Base):
    __tablename__ = "raw_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    event_type = Column(String, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=True, index=True)
    
    # Using JSON for metadata to support flexible event-driven data
    metadata_json = Column(JSON, nullable=True)

    user = relationship("User", back_populates="events")
    habit = relationship("Habit", back_populates="events")
