#!/usr/bin/env python3
"""
Initialize the LifeFlow database with schema and test data.
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path so we can import the app module
sys.path.insert(0, str(Path(__file__).parent))
print(f"Added {str(Path(__file__).parent)} to Python path")

from app.init_db import init_db
from app.models.user import User
from app.database import SessionLocal

def create_test_user():
    """Create a test user if one doesn't exist."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == 1).first()
        if not user:
            user = User(
                id=1, 
                email="test@example.com",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
                is_active=True
            )
            db.add(user)
            db.commit()
            print("👤 Created test user (id: 1, email: test@example.com)")
        else:
            print("👤 Test user already exists.")
    except Exception as e:
        print(f"⚠️ Error creating test user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🗃️ Initializing database...")
    init_db()
    print("✅ Database schema created successfully.")
    
    print("🔄 Creating test data...")
    create_test_user()
    print("✅ Test data created successfully.")
    
    print("🚀 Database initialized and ready to use!")
