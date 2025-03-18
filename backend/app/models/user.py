"""
User model for the database.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """User model for storing user account information."""

    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # User Information
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transactions = relationship("Transaction", back_populates="user")
    personality_profile = relationship("PersonalityProfile", back_populates="user", uselist=False) 