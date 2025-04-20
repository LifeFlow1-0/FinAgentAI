from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, JSON
from . import Base

class OnboardingSession(Base):
    """Model for storing onboarding session data."""
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=7))
    data = Column(JSON, default=dict)          # answers cache 