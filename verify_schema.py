from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.habit import Habit
from app.models.event import Event
from sqlalchemy.sql import func

def verify():
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

    db = SessionLocal()
    try:
        # 1. Create a user
        user = User(email="test@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"User created: {user.id}, {user.email}")

        # 2. Create a habit
        habit = Habit(name="Read 30 mins", user_id=user.id)
        db.add(habit)
        db.commit()
        db.refresh(habit)
        print(f"Habit created: {habit.id}, {habit.name}")

        # 3. Log events
        event1 = Event(
            event_type="habit_created",
            user_id=user.id,
            habit_id=habit.id,
            metadata_json={"source": "api_v1"}
        )
        event2 = Event(
            event_type="habit_completed",
            user_id=user.id,
            habit_id=habit.id,
            metadata_json={"duration_seconds": 1800}
        )
        db.add(event1)
        db.add(event2)
        db.commit()
        print("Events logged.")

        # 4. Query events
        events = db.query(Event).filter(Event.user_id == user.id).all()
        print(f"Queried {len(events)} events for user {user.id}:")
        for e in events:
            print(f"- {e.event_type} at {e.timestamp} with metadata {e.metadata_json}")

    finally:
        db.close()

if __name__ == "__main__":
    verify()
