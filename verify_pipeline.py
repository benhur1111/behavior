from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.habit import Habit
from app.models.raw_event import RawEvent
from app.models.analytics import DailyAggregate, UserBehaviorMetric
from app.pipeline.run_pipeline import run_etl
from datetime import datetime, timedelta

def verify_pipeline():
    # 1. Reset database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database reset.")

    db = SessionLocal()
    try:
        # 2. Seed data
        user = User(email="data_eng@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        
        habit = Habit(name="Deep Work", user_id=user.id)
        db.add(habit)
        db.commit()
        db.refresh(habit)
        
        # Multiple days of data
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        events = [
            RawEvent(event_type="habit_started", user_id=user.id, habit_id=habit.id, timestamp=yesterday),
            RawEvent(event_type="habit_completed", user_id=user.id, habit_id=habit.id, timestamp=yesterday),
            RawEvent(event_type="habit_started", user_id=user.id, habit_id=habit.id, timestamp=today),
            RawEvent(event_type="habit_skipped", user_id=user.id, habit_id=habit.id, timestamp=today),
        ]
        db.add_all(events)
        db.commit()
        print("Seeded test data spanning 2 days.")
        
        # 3. Run ETL
        run_etl()
        
        # 4. Verify aggregates
        aggregates = db.query(DailyAggregate).all()
        print(f"\nDaily Aggregates ({len(aggregates)}):")
        for agg in aggregates:
            print(f"- {agg.date}: {agg.event_type} = {agg.count}")
            
        # 5. Verify metrics
        metrics = db.query(UserBehaviorMetric).all()
        print(f"\nUser Metrics ({len(metrics)}):")
        for m in metrics:
            print(f"- User {m.user_id}: {m.metric_name} = {m.metric_value}")
            
    finally:
        db.close()

if __name__ == "__main__":
    verify_pipeline()
