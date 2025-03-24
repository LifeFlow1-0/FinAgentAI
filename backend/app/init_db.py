"""
Initialize database and create tables.
"""
from sqlalchemy import text
from app.database import Base, engine

def init_db():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)
    
    # Create a test user directly with SQL if it doesn't exist
    with engine.connect() as conn:
        # Check if table exists
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'"))
        if result.fetchone():
            # Check if test user exists
            result = conn.execute(text("SELECT id FROM users WHERE id = 1"))
            if not result.fetchone():
                # Create test user
                conn.execute(text("""
                    INSERT INTO users (id, email, hashed_password, is_active, created_at, updated_at)
                    VALUES (
                        1, 
                        'test@example.com', 
                        '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 
                        1,
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
                print("Test user created.")
            else:
                print("Test user already exists.")
        else:
            print("Users table doesn't exist yet.")

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.") 