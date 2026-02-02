from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.habit import Habit
    from app.models.raw_event import RawEvent

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    habits = relationship("Habit", back_populates="owner")
    events = relationship("RawEvent", back_populates="user")
