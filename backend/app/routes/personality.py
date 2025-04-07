"""
API routes for personality profile operations.
"""

from datetime import datetime
from typing import Optional
import logging
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.database import get_db
from app.models.personality import PersonalityProfile
from app.models.user import User
from app.schemas.personality import PersonalityProfileCreate, PersonalityProfileResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Update router prefix to remove duplicate /api/v1
router = APIRouter(prefix="/user-profile/personality", tags=["personality"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_personality_profile(
    profile: PersonalityProfileCreate,
    db: Session = Depends(get_db),
    x_user_id: Optional[str] = Header(None)
):
    """Create a new personality profile for a user."""
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-User-ID header is required"
        )
    
    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    logger.info(f"Looking for user with ID: {user_id}")
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    logger.info(f"User query result: {user}")
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if profile already exists
    existing_profile = db.query(PersonalityProfile).filter(
        PersonalityProfile.user_id == user_id
    ).first()
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Personality profile already exists for this user"
        )

    try:
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
        
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)

        # Return success response
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "status": "success",
                "id": str(new_profile.id)
            }
        )

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{user_id}", response_model=PersonalityProfileResponse)
async def get_personality_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get a user's personality profile."""
    profile = (
        db.query(PersonalityProfile)
        .filter(PersonalityProfile.user_id == user_id)
        .first()
    )
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personality profile not found"
        )
    
    return PersonalityProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
        **profile.get_personality_data()
    ) 