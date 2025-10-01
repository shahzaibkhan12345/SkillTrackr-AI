# agent/crud/crud_plan.py

from sqlalchemy.orm import Session
from agent.models.schemas import PlanCreate, TaskCreate, TaskUpdate
from agent.database import Plan, Task
import json

# --- CRUD Operations for Plans ---

def create_plan(db: Session, plan: PlanCreate):
    """Creates a new plan in the database."""
    db_plan = Plan(goal=plan.goal, duration_weeks=plan.duration_weeks)
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def get_plan(db: Session, plan_id: int):
    """Gets a single plan by its ID."""
    return db.query(Plan).filter(Plan.id == plan_id).first()

def get_plans(db: Session, skip: int = 0, limit: int = 100):
    """Gets a list of all plans."""
    return db.query(Plan).offset(skip).limit(limit).all()

# --- CRUD Operations for Tasks ---

def create_task_for_plan(db: Session, task: TaskCreate, plan_id: int):
    """Creates a new task and links it to a plan."""
    # Convert list of URLs to a JSON string for storage
    resource_links_json = json.dumps([url.unicode_string() for url in task.resource_links])
    
    db_task = Task(
        plan_id=plan_id,
        week_number=task.week_number,
        title=task.title,
        description=task.description,
        resource_links=resource_links_json
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task_status(db: Session, task_id: int, task_update: TaskUpdate):
    """Updates the completion status of a task."""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.is_completed = task_update.is_completed
        db.commit()
        db.refresh(db_task)
    return db_task