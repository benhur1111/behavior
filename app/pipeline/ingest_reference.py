import pandas as pd
from app.core.database import SessionLocal, engine, Base
from app.models.analytics import ReferenceExerciseBenchmark
import os

def ingest_reference_data():
    csv_path = "exercise_reference.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    # 1. Read CSV
    df = pd.read_csv(csv_path)
    
    # Clean duration (e.g., '1 min' -> 1)
    df["duration_min"] = df["time"].str.extract("(\d+)").astype(int)
    
    # 2. Setup DB
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # 3. Clear existing reference data
        db.query(ReferenceExerciseBenchmark).delete()
        
        # 4. Load into DB
        print(f"Ingesting {len(df)} records from {csv_path}...")
        for _, row in df.iterrows():
            benchmark = ReferenceExerciseBenchmark(
                participant_id=int(row["id"]),
                diet=row["diet"],
                pulse=int(row["pulse"]),
                duration_min=int(row["duration_min"]),
                activity_kind=row["kind"]
            )
            db.add(benchmark)
        
        db.commit()
        print("Reference data ingestion complete.")
        
    finally:
        db.close()

if __name__ == "__main__":
    ingest_reference_data()
