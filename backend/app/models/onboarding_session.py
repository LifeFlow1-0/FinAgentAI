from app.models.base import Base
from sqlalchemy import Column, String, DateTime, JSON
import uuid, datetime as dt

def _expires(ttl_mins: int = 7 * 24 * 60):  # default 7 days
    return dt.datetime.utcnow() + dt.timedelta(minutes=ttl_mins)

class OnboardingSession(Base):
    __tablename__ = "sessions"

    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, default=_expires, nullable=False)
    data       = Column(JSON, default=dict)          # answers cache 