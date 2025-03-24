"""
Database connection and session management.
"""

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Create SQLite database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{settings.DATABASE_PATH}"

# Create engine with SQLite connect_args for thread safety
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    # Echo SQL for debugging in dev mode
    echo=settings.DEBUG
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Import all models here to ensure they're discovered 
# when Base.metadata.create_all() is called
# This avoids circular import issues when importing individual models
from app.models.user import User
from app.models.transaction import Transaction
from app.models.plaid import PlaidItem, PlaidAccount
from app.models.personality import PersonalityProfile

def get_db():
    """Get database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
