"""
Initialize database and create tables.
"""
from app.database import Base, engine
from app.models.user import User
from app.models.transaction import Transaction
from app.models.plaid import PlaidItem, PlaidAccount

def init_db():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.") 