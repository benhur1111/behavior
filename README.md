# Behavior Analytics Data Platform

A professional event-driven data platform designed to track, process, and analyze behavioral patterns for habit-building and productivity.

## 🏗️ Data Architecture

The platform follows a modern **Medallion Architecture** to ensure data quality and scalability:

### 1. Ingestion Layer (Landing/Landing Zone)
- **Framework**: FastAPI
- **Endpoints**: `/events` and `/events/batch`
- **Function**: Capture high-frequency behavioral events (e.g., `habit_started`, `habit_completed`) with flexible JSON metadata.

### 2. Bronze Layer (Raw Storage)
- **Schema**: `raw_events` table (SQLAlchemy/SQLite)
- **Data Model**: Append-only log preserving original event structure and metadata.

### 3. Silver Layer (Processing/ETL)
- **Engine**: Pandas (Python Data Analysis Library)
- **Pipeline**: `app/pipeline/run_pipeline.py`
- **Logic**: Modular Extract-Transform-Load (ETL) process that cleanses and aggregates raw data into behavioral entities.

### 4. Gold Layer (Analytics/Consumption)
- **Tables**: 
    - `daily_aggregates`: Time-series summaries of event frequencies.
    - `user_behavior_metrics`: High-level behavioral insights (Consistency, Risk, Performance).
    - `reference_exercise_benchmarks`: External industry data for comparative analysis.

---

## 🚀 Pipeline & Transformations

### ETL Workflow
1. **Extraction**: Efficiently pulls raw events into Pandas DataFrames.
2. **Transformation**:
    - **Vectorized Operations**: High-performance calculation of activity counts.
    - **Sessionization**: Pairs `started` and `completed` events to compute exact durations.
    - **Temporal Analysis**: Analyzes activity windows to determine consistency and churn risk.
3. **Loading**: Performs idempotent upserts into analytics-ready tables.

### Advanced Metrics
- **Consistency Score**: A 7-day rolling window measuring user engagement regularity.
- **Dropout Probability**: A predictive metric assessing user churn risk based on inactivity thresholds.
- **Average Completion Time**: Precise measurement of "effort" per habit execution.

---

## 🔍 Analytics Use Cases

| Feature | Description | Business Value |
|---------|-------------|----------------|
| **Retention Analysis** | Monitors `dropout_probability` across user segments. | Enables proactive nudges to prevent churn. |
| **Comparative Benchmarking** | Joins user performance with `reference_exercise_benchmarks`. | Provides users with scientific context for their progress. |
| **Habit Streaks** | Uses `consistency_score` to validate streak validity. | Gamifies productivity and drives daily engagement. |

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.8+
- SQLite (Local development)

### Running the Pipeline
```bash
# Set PYTHONPATH
export PYTHONPATH=.

# Run the ETL Pipeline
python app/pipeline/run_pipeline.py

# Run Ingestion Verification
python verify_pipeline.py
```

### Ingesting External Data
```bash
python app/pipeline/ingest_reference.py
```
