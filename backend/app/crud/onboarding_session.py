from sqlalchemy.orm import Session
from app.models.onboarding_session import OnboardingSession
import datetime as dt, uuid

def create_session(db: Session, ttl_mins: int = 7*24*60):
    obj = OnboardingSession(id=str(uuid.uuid4()),
                            expires_at=dt.datetime.utcnow() + dt.timedelta(minutes=ttl_mins))
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def get_session(db: Session, sid: str):
    return db.query(OnboardingSession).filter(OnboardingSession.id == sid).first()

def patch_data(db: Session, sid: str, delta: dict):
    sess = get_session(db, sid)
    if not sess:
        return None
    sess.data.update(delta)
    db.commit(); db.refresh(sess)
    return sess 