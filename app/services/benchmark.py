from sqlalchemy.orm import Session
from app.models.raw_event import RawEvent
from app.models.analytics import ReferenceExerciseBenchmark
from sqlalchemy import func

def get_benchmark_comparison(db: Session, user_id: int, activity_type: str):
    """
    Comparison logic: Joins user's average performance (if available in metadata)
    or just frequency against the reference benchmark.
    """
    
    # 1. Get reference stats for this activity
    ref_stats = db.query(
        func.avg(ReferenceExerciseBenchmark.pulse).label("avg_pulse"),
        func.avg(ReferenceExerciseBenchmark.duration_min).label("avg_duration")
    ).filter(ReferenceExerciseBenchmark.activity_kind == activity_type).first()
    
    if not ref_stats or ref_stats.avg_pulse is None:
        return {"error": f"No reference data found for activity: {activity_type}"}

    # 2. Get user's events for this activity to see their history
    # Joining app data (RawEvent metadata) with reference data (activity_kind)
    user_events = db.query(RawEvent).filter(
        RawEvent.user_id == user_id,
        func.json_extract(RawEvent.metadata_json, "$.activity_type") == activity_type
    ).all()
    
    completions = len(user_events)
    
    return {
        "activity": activity_type,
        "reference_avg_pulse": round(float(ref_stats.avg_pulse), 2),
        "reference_avg_duration": round(float(ref_stats.avg_duration), 2),
        "user_completion_count": completions,
        "insight": f"You have tracked {activity_type} {completions} times. "
                   f"Reference group for '{activity_type}' averages {round(float(ref_stats.avg_pulse), 1)} BPM pulse."
    }
