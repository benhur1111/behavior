import pandas as pd
from typing import Tuple

def transform_daily_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """Group events by day and type to get counts."""
    if df.empty:
        return pd.DataFrame()
    
    # Extract date from timestamp
    df["date"] = df["timestamp"].dt.date
    
    # Aggregate counts
    aggregates = df.groupby(["date", "event_type"]).size().reset_index(name="count")
    return aggregates

def transform_user_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate per-user metrics including advanced ones."""
    if df.empty:
        return pd.DataFrame()
    
    metrics_list = []
    now = pd.Timestamp.now()
    
    # User-level aggregation
    user_groups = df.groupby("user_id")
    
    for user_id, group in user_groups:
        uid = int(user_id)
        
        # 1. Total activities
        metrics_list.append({
            "user_id": uid,
            "metric_name": "total_activities",
            "metric_value": float(len(group))
        })
        
        # 2. Total completions
        completions = len(group[group["event_type"] == "habit_completed"])
        metrics_list.append({
            "user_id": uid,
            "metric_name": "total_completions",
            "metric_value": float(completions)
        })
        
        # 3. Active days
        active_days = group["timestamp"].dt.date.nunique()
        metrics_list.append({
            "user_id": uid,
            "metric_name": "active_days",
            "metric_value": float(active_days)
        })

        # --- Advanced Metrics ---

        # 4. Consistency Score (last 7 days)
        last_7_days = now - pd.Timedelta(days=7)
        recent_group = group[group["timestamp"] >= last_7_days]
        days_active_recent = recent_group["timestamp"].dt.date.nunique()
        consistency_score = (days_active_recent / 7.0) * 100
        metrics_list.append({
            "user_id": uid,
            "metric_name": "consistency_score",
            "metric_value": float(consistency_score)
        })

        # 5. Dropout Probability
        last_activity = group["timestamp"].max()
        days_since_active = (now - last_activity).days
        
        if days_since_active <= 1:
            dropout_prob = 5.0
        elif days_since_active <= 3:
            dropout_prob = 25.0
        elif days_since_active <= 7:
            dropout_prob = 60.0
        else:
            dropout_prob = 90.0
            
        metrics_list.append({
            "user_id": uid,
            "metric_name": "dropout_probability",
            "metric_value": float(dropout_prob)
        })

        # 6. Average Completion Time (per habit)
        # We look for (habit_started, habit_completed) pairs for the same habit_id
        avg_times = []
        habit_groups = group.groupby("habit_id")
        for habit_id, h_group in habit_groups:
            if pd.isna(habit_id): continue
            h_group = h_group.sort_values("timestamp")
            
            # Find pairs
            starts = h_group[h_group["event_type"] == "habit_started"]
            completes = h_group[h_group["event_type"] == "habit_completed"]
            
            for _, s_row in starts.iterrows():
                # Find the next completion for this habit
                next_c = completes[completes["timestamp"] > s_row["timestamp"]].head(1)
                if not next_c.empty:
                    duration = (next_c.iloc[0]["timestamp"] - s_row["timestamp"]).total_seconds()
                    avg_times.append(duration)
        
        if avg_times:
            avg_comp_time = sum(avg_times) / len(avg_times)
            metrics_list.append({
                "user_id": uid,
                "metric_name": "avg_completion_time_seconds",
                "metric_value": float(avg_comp_time)
            })
        
    return pd.DataFrame(metrics_list)
