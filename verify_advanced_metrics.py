from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.habit import Habit
from app.models.raw_event import RawEvent
from app.models.analytics import UserBehaviorMetric
from app.pipeline.run_pipeline import run_etl
from datetime import datetime, timedelta
import pandas as pd

def verify_advanced_analytics():
    # 1. Reset database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database reset.")

    db = SessionLocal()
    try:
        # 2. Seed data for User
        user = User(email="analytics_pro@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        
        habit = Habit(name="Meditation", user_id=user.id)
        db.add(habit)
        db.commit()
        db.refresh(habit)
        
        now = datetime.now()
        
        # Scenario A: Test Consistency & Dropout
        # We'll seed 3 days of activity in the last 7 days.
        # Last activity was 2 days ago -> Dropout Prob should be 25% (Early signs)
        events = [
            # 5 days ago
            RawEvent(event_type="habit_completed", user_id=user.id, habit_id=habit.id, 
                     timestamp=now - timedelta(days=5), metadata_json={"activity_type": "meditation"}),
            # 4 days ago
            RawEvent(event_type="habit_completed", user_id=user.id, habit_id=habit.id, 
                     timestamp=now - timedelta(days=4), metadata_json={"activity_type": "meditation"}),
            # 2 days ago (Last activity)
            RawEvent(event_type="habit_completed", user_id=user.id, habit_id=habit.id, 
                     timestamp=now - timedelta(days=2), metadata_json={"activity_type": "meditation"}),
        ]
        
        # Scenario B: Test Average Completion Time
        # Start at 10:00, Complete at 10:15 (900 seconds)
        # Start at 11:00, Complete at 11:05 (300 seconds)
        # Average should be 600 seconds.
        events.extend([
            RawEvent(event_type="habit_started", user_id=user.id, habit_id=habit.id, 
                     timestamp=now - timedelta(hours=1, minutes=30), metadata_json={"activity_type": "meditation"}),
            RawEvent(event_type="habit_completed", user_id=user.id, habit_id=habit.id, 
                     timestamp=now - timedelta(hours=1, minutes=15), metadata_json={"activity_type": "meditation"}),
            
            RawEvent(event_type="habit_started", user_id=user.id, habit_id=habit.id, 
                     timestamp=now - timedelta(minutes=6), metadata_json={"activity_type": "meditation"}),
            RawEvent(event_type="habit_completed", user_id=user.id, habit_id=habit.id, 
                     timestamp=now - timedelta(minutes=1), metadata_json={"activity_type": "meditation"}),
        ])
        
        db.add_all(events)
        db.commit()
        print("Seeded test data for advanced metrics.")
        
        # 3. Run ETL
        run_etl()
        
        # 4. Verify results
        metrics = db.query(UserBehaviorMetric).all()
        print(f"\nAdvanced User Metrics ({len(metrics)}):")
        for m in metrics:
            print(f"- {m.metric_name}: {m.metric_value}")
            
        # Specific assertions (Manual review in output)
        # Expect:
        # consistency_score (~42.8% if 3 distinct days in 7)
        # dropout_probability (25.0 if last activity was 2 days ago)
        # avg_completion_time_seconds (600.0)

    finally:
        db.close()

if __name__ == "__main__":
    verify_advanced_analytics()
