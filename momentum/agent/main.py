# agent/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from contextlib import asynccontextmanager

# Import our project's modules
from agent.database import get_db, create_db_and_tables
from agent.models import schemas
from agent.crud import crud_plan
from agent.core import config
# Import the new planner function
from agent.core.planner import generate_plan_with_ai


# --- Lifespan handler (replaces @app.on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    create_db_and_tables()
    print("✅ Database tables are ready.")
    print("🚀 Momentum Agent API is live!")

    yield  # <-- App runs while inside this block

    # --- Shutdown ---
    print("👋 Shutting down Momentum Agent API...")


# --- Create the FastAPI App Instance ---
app = FastAPI(
    title="Momentum Agent API",
    description="The backend API for the Momentum personal growth agent.",
    version="0.1.0",
    lifespan=lifespan
)


# --- API Endpoints ---

# Endpoint to create a new plan
# Endpoint to create a new plan
@app.post("/plans/", response_model=schemas.Plan)
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    """
    Takes a goal and duration, uses AI to generate a plan,
    and saves it to the database.
    """
    print(f"🚀 Received request to create a plan for: '{plan.goal}'")
    
    # 1. Create the plan shell in the database first
    db_plan = crud_plan.create_plan(db=db, plan=plan)
    
    print("🧠 Calling the AI to generate tasks... This might take a moment.")
    # 2. Use the AI to generate the tasks for the plan
    generated_tasks = generate_plan_with_ai(plan=plan)
    print("✅ AI generation complete.")
    
    # 3. Save each generated task to the database, linked to the plan
    for task in generated_tasks:
        crud_plan.create_task_for_plan(db=db, task=task, plan_id=db_plan.id)
        
    # 4. Refresh the plan object to include the new tasks before returning
    db.refresh(db_plan)
    
    print("💾 Plan and tasks saved to database. Sending response.")
    return db_plan


# Endpoint to get a specific plan by its ID, including all its tasks
@app.get("/plans/{plan_id}", response_model=schemas.Plan)
def read_plan(plan_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single plan and all its associated tasks.
    """
    db_plan = crud_plan.get_plan(db=db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return db_plan


# Endpoint to get a list of all plans
@app.get("/plans/", response_model=List[schemas.Plan])
def read_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of all plans from the database.
    """
    plans = crud_plan.get_plans(db=db, skip=skip, limit=limit)
    return plans


# Endpoint to update the status of a task (e.g., mark as complete)
@app.patch("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """
    Updates the completion status of a specific task.
    """
    db_task = crud_plan.update_task_status(db=db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


# A simple root endpoint to confirm the API is running
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Momentum Agent API. See /docs for more information."}
