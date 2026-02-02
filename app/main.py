from fastapi import FastAPI
from app.api import health, behaviors, events
from app import models

app = FastAPI(title="Behavior Change Tracker")

app.include_router(health.router)
app.include_router(behaviors.router)
app.include_router(events.router)
