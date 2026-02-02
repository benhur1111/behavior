from sqlalchemy.orm import Session
from app.models.analytics import DailyAggregate, UserBehaviorMetric
import pandas as pd

def load_daily_aggregates(db: Session, df: pd.DataFrame):
    """Upsert daily aggregates into the database."""
    if df.empty:
        return

    for _, row in df.iterrows():
        # Check if already exists for this date and type
        existing = db.query(DailyAggregate).filter(
            DailyAggregate.date == row["date"],
            DailyAggregate.event_type == row["event_type"]
        ).first()
        
        if existing:
            existing.count = int(row["count"])
        else:
            agg = DailyAggregate(
                date=row["date"],
                event_type=row["event_type"],
                count=int(row["count"])
            )
            db.add(agg)
    db.commit()

def load_user_metrics(db: Session, df: pd.DataFrame):
    """Upsert user behavior metrics into the database."""
    if df.empty:
        return

    for _, row in df.iterrows():
        # Check if already exists for this user and metric
        existing = db.query(UserBehaviorMetric).filter(
            UserBehaviorMetric.user_id == row["user_id"],
            UserBehaviorMetric.metric_name == row["metric_name"]
        ).first()
        
        if existing:
            existing.metric_value = float(row["metric_value"])
        else:
            metric = UserBehaviorMetric(
                user_id=int(row["user_id"]),
                metric_name=row["metric_name"],
                metric_value=float(row["metric_value"])
            )
            db.add(metric)
    db.commit()
