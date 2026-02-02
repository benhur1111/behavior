from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.raw_event import RawEvent
from app.pipeline.ingest_reference import ingest_reference_data
from app.services.benchmark import get_benchmark_comparison

def verify_external_ingestion():
    # 1. Ingest reference data
    ingest_reference_data()

    db = SessionLocal()
    try:
        # 2. Create a test user if not exists
        user = db.query(User).filter(User.email == "bench_test@example.com").first()
        if not user:
            user = User(email="bench_test@example.com")
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # 3. Add some app-generated events
        # Simulate a few 'running' completions
        test_user_id = user.id
        events = [
            RawEvent(event_type="habit_completed", user_id=test_user_id, metadata_json={"activity_type": "running"}),
            RawEvent(event_type="habit_completed", user_id=test_user_id, metadata_json={"activity_type": "running"}),
        ]
        db.add_all(events)
        db.commit()
        print(f"Seeded 2 test events for user {test_user_id} with activity_type 'running'.")

        # Debug: check all events
        all_ev = db.query(RawEvent).filter(RawEvent.user_id == test_user_id).all()
        print(f"Total events for user: {len(all_ev)}")
        for e in all_ev:
            print(f"- Type: {e.event_type}, Metadata: {e.metadata_json}")

        # 4. Perform the Join/Comparison
        print("\n--- Benchmark Integration Result ---")
        comparison = get_benchmark_comparison(db, test_user_id, "running")
        print(comparison)

    finally:
        db.close()

if __name__ == "__main__":
    verify_external_ingestion()
