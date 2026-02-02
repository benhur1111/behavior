from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class DailyAggregate(Base):
    __tablename__ = "daily_aggregates"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True, nullable=False)
    event_type = Column(String, index=True, nullable=False)
    count = Column(Integer, default=0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class UserBehaviorMetric(Base):
    __tablename__ = "user_behavior_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    metric_name = Column(String, index=True, nullable=False)
    metric_value = Column(Float, default=0.0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ReferenceExerciseBenchmark(Base):
    __tablename__ = "reference_exercise_benchmarks"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, index=True)
    diet = Column(String)
    pulse = Column(Integer)
    duration_min = Column(Integer)
    activity_kind = Column(String, index=True) # rest, walking, running
