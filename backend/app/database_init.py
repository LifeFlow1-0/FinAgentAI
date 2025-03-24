#!/usr/bin/env python3
"""
Database initialization script for LifeFlow.
Runs inside the Docker container.
"""
from app.init_db import init_db
from app.models.user import User
from app.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_user():
    """Create a test user if one doesn't exist."""
    db = SessionLocal()
    try:
        logger.info("Checking if test user exists...")
        user = db.query(User).filter(User.id == 1).first()
        if not user:
            logger.info("Creating test user...")
            test_user = User(
                id=1, 
                email="test@example.com",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
                is_active=True
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            logger.info(f"Created test user (id: {test_user.id}, email: {test_user.email})")
        else:
            logger.info(f"Test user already exists (id: {user.id}, email: {user.email})")
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
    except Exception as e:
        logger.error(f"Error creating test user: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()
    logger.info("Database schema created successfully.")
    
    logger.info("Creating test data...")
    create_test_user()
    logger.info("Database initialized and ready to use!") 