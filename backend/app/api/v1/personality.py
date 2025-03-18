from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.models.personality import PersonalityProfile
from app.schemas.personality import PersonalityProfileCreate, PersonalityProfileResponse

router = APIRouter()

@router.post("/user-profile/personality", status_code=201, response_model=PersonalityProfileResponse)
def create_personality_profile(
    profile: PersonalityProfileCreate,
    db: Session = Depends(get_db),
    x_user_id: Optional[str] = Header(None)
):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-ID header is required")
    
    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    # Check if profile already exists
    existing_profile = db.query(PersonalityProfile).filter(
        PersonalityProfile.user_id == user_id
    ).first()
    
    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="Personality profile already exists for this user"
        )

    # Create new profile
    new_profile = PersonalityProfile(
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Set encrypted personality data
    new_profile.set_personality_data({
        "openness": profile.openness,
        "social_energy": profile.social_energy,
        "learning_style": profile.learning_style,
        "activity_intensity": profile.activity_intensity
    })
    
    try:
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Could not create personality profile: {str(e)}"
        )
    
    # Return decrypted data
    return PersonalityProfileResponse(
        id=new_profile.id,
        user_id=new_profile.user_id,
        **new_profile.get_personality_data(),
        created_at=new_profile.created_at,
        updated_at=new_profile.updated_at
    ) 