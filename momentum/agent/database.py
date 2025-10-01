# agent/database.py

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# --- Database URL ---
# We use a file-based SQLite database. It will be created in the 'data' folder.
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/momentum.db"

# --- Database Engine ---
# The engine is the starting point for any SQLAlchemy application.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# --- Session Factory ---
# Each instance of SessionLocal will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Base Model ---
# All our ORM models will inherit from this Base class.
Base = declarative_base()

# --- ORM Models (These define the database tables) ---

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    goal = Column(String, index=True)
    duration_weeks = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # This creates a relationship to the Task table.
    # "back_populates" creates a two-way relationship.
    tasks = relationship("Task", back_populates="plan", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"))
    week_number = Column(Integer)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    resource_links = Column(String, nullable=True) # Store as a JSON string
    is_completed = Column(Boolean, default=False)

    # This creates the other side of the relationship to the Plan table.
    plan = relationship("Plan", back_populates="tasks")


# --- Function to create the database tables ---
def create_db_and_tables():
    """
    This function will create the database file and the tables
    if they don't exist already.
    """
    Base.metadata.create_all(bind=engine)

# --- Dependency to get a DB session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()