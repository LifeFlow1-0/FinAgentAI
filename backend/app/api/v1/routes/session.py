from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db  # Updated import path
from app.schemas.onboarding_session import SessionOut
from app.crud.onboarding_session import create_session, get_session

router = APIRouter(prefix="/session", tags=["onboarding"])

@router.post("", response_model=SessionOut, status_code=201)
def new_session(db: Session = Depends(get_db)):
    return create_session(db)

@router.get("/{sid}", response_model=SessionOut)
def fetch_session(sid: str, db: Session = Depends(get_db)):
    sess = get_session(db, sid)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    return sess 