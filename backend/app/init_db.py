"""
Initialize database and create tables with environment-specific configuration.
"""
import os
import time
import logging
from typing import Optional
from sqlalchemy import text, inspect
from sqlalchemy.exc import SQLAlchemyError
from alembic import command
from alembic.config import Config
from app.database import Base, engine, SessionLocal
from app.models.user import User
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_environment() -> str:
    """Get the current environment."""
    return os.getenv("ENVIRONMENT", "development")

def check_database_health() -> bool:
    """Check if database is accessible and healthy."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database health check failed: {str(e)}")
        return False

def create_test_user(environment: str) -> Optional[User]:
    """Create a test user if one doesn't exist."""
    if environment == "production":
        logger.info("Skipping test user creation in production environment")
        return None

    db = SessionLocal()
    start_time = time.time()
    try:
        logger.info("Checking if test user exists...")
        user = db.query(User).filter(User.id == 1).first()
        if not user:
            logger.info("Creating test user...")
            test_user = User(
                id=1,
                email=os.getenv("TEST_USER_EMAIL", "test@example.com"),
                hashed_password=os.getenv("TEST_USER_PASSWORD", "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"),
                is_active=True
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            logger.info(f"Created test user (id: {test_user.id}, email: {test_user.email})")
            return test_user
        else:
            logger.info(f"Test user already exists (id: {user.id}, email: {user.email})")
            return user
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error creating test user: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()
        duration = time.time() - start_time
        logger.info(f"Test user creation completed in {duration:.2f} seconds")

def get_database_stats() -> dict:
    """Get database statistics."""
    inspector = inspect(engine)
    stats = {
        "tables": len(inspector.get_table_names()),
        "columns": sum(len(inspector.get_columns(table)) for table in inspector.get_table_names()),
        "indexes": sum(len(inspector.get_indexes(table)) for table in inspector.get_table_names())
    }
    return stats

def init_db() -> None:
    """Create all tables and initialize test data with environment-specific configuration."""
    start_time = time.time()
    environment = get_environment()
    
    try:
        # Check database health
        if not check_database_health():
            raise SQLAlchemyError("Database health check failed")

        logger.info(f"Starting database initialization for {environment} environment...")
        
        # Run Alembic migrations
        logger.info("Running database migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully.")
        
        # Create test data if not in production
        if environment != "production":
            logger.info("Creating test data...")
            create_test_user(environment)
            logger.info("Test data created successfully.")
        
        # Log database statistics
        stats = get_database_stats()
        logger.info(f"Database statistics: {stats}")
        
        duration = time.time() - start_time
        logger.info(f"Database initialization completed in {duration:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    init_db()
    logger.info("Database initialized successfully.") 