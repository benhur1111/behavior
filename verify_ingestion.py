import requests
import time
import subprocess
import os
import signal

def run_test():
    # 1. Initialize DB (create tables)
    from app.core.database import engine, Base
    from app.models.user import User
    from app.models.habit import Habit
    from app.models.raw_event import RawEvent
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database reset and tables created.")

    # 2. Add a test user and habit directly for testing the API
    from app.core.database import SessionLocal
    db = SessionLocal()
    user = User(email="api_test@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    habit = Habit(name="Coding", user_id=user.id)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    user_id = user.id
    habit_id = habit.id
    db.close()
    print(f"Test user (ID: {user_id}) and habit (ID: {habit_id}) created.")

    # 3. Start FastAPI server
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    server_process = subprocess.Popen(
        [".venv/bin/python", "-m", "uvicorn", "app.main:app", "--port", "8008"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5) # Wait for server to start

    try:
        # 4. Send single event ingestion request
        payload = {
            "event_type": "habit_started",
            "user_id": user_id,
            "habit_id": habit_id,
            "metadata_json": {"platform": "mobile"}
        }
        response = requests.post("http://localhost:8008/events", json=payload)
        print(f"Single event response: {response.status_code}, {response.json()}")

        # 5. Send batch event ingestion request
        batch_payload = [
            {
                "event_type": "habit_completed",
                "user_id": user_id,
                "habit_id": habit_id,
                "metadata_json": {"duration": 3600}
            },
            {
                "event_type": "habit_skipped",
                "user_id": user_id,
                "metadata_json": {"reason": "tired"}
            }
        ]
        response = requests.post("http://localhost:8008/events/batch", json=batch_payload)
        print(f"Batch event response: {response.status_code}, {response.json()}")

        # 6. Verify in DB
        db = SessionLocal()
        events = db.query(RawEvent).all()
        print(f"Total events in raw_events table: {len(events)}")
        for e in events:
            print(f"- {e.event_type} (User: {e.user_id}, Habit: {e.habit_id})")
        db.close()

    finally:
        os.kill(server_process.pid, signal.SIGTERM)
        print("Server stopped.")

if __name__ == "__main__":
    run_test()
