from pydantic import BaseModel
from datetime import date

class Behavior(BaseModel):
    name: str
    date: date
    completed: bool
