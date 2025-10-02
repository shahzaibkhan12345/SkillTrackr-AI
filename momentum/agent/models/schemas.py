# agent/models/schemas.py

from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

# --- Base Schemas ---
class PlanBase(BaseModel):
    goal: str
    duration_weeks: int

class TaskBase(BaseModel):
    week_number: int
    title: str
    description: Optional[str] = None
    resource_links: List[HttpUrl] = []

# --- Schemas for API Requests/Responses ---

# For creating a new plan
class PlanCreate(PlanBase):
    pass

# 👇 --- ADD THIS LINE --- 👇
# For creating a new task
class TaskCreate(TaskBase):
    pass

# For the full plan data sent back to the UI
class Plan(PlanBase):
    id: int
    created_at: datetime
    tasks: List['Task'] = []

    class Config:
        from_attributes = True # Allows Pydantic to read data from ORM models

# For a single task
class Task(TaskBase):
    id: int
    plan_id: int
    is_completed: bool = False

    class Config:
        from_attributes = True

# For updating a task's status
class TaskUpdate(BaseModel):
    is_completed: bool