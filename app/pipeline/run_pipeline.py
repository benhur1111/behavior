from app.core.database import SessionLocal
from app.pipeline.extract import extract_raw_events
from app.pipeline.transform import transform_daily_aggregates, transform_user_metrics
from app.pipeline.load import load_daily_aggregates, load_user_metrics

def run_etl():
    """Run the complete ETL pipeline."""
    db = SessionLocal()
    try:
        print("Extracting raw events...")
        df_raw = extract_raw_events(db)
        print(f"Extracted {len(df_raw)} records.")
        
        if df_raw.empty:
            print("No data to process.")
            return

        print("Transforming data...")
        df_daily = transform_daily_aggregates(df_raw)
        df_user_metrics = transform_user_metrics(df_raw)
        
        print("Loading daily aggregates...")
        load_daily_aggregates(db, df_daily)
        
        print("Loading user behavior metrics...")
        load_user_metrics(db, df_user_metrics)
        
        print("ETL Pipeline completed successfully.")
        
    finally:
        db.close()

if __name__ == "__main__":
    run_etl()
