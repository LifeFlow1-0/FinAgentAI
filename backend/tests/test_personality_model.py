from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest
from fastapi import status
from app.main import app
from app.models.personality import PersonalityProfile
from datetime import datetime

client = TestClient(app)

def test_valid_personality_input(client, test_user):
    data = {
        "openness": "c",  # Explorer
        "social_energy": "a",  # Introvert
        "learning_style": "b",  # Mixed
        "activity_intensity": "c"  # Dynamic
    }
    response = client.post(
        "/api/v1/user-profile/personality",
        json=data,
        headers={"X-User-ID": str(test_user.id)}
    )
    assert response.status_code == status.HTTP_201_CREATED
    
    # Verify data using API
    get_response = client.get(f"/api/v1/user-profile/personality/{test_user.id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["openness"] == "c"
    assert get_response.json()["social_energy"] == "a"
    assert get_response.json()["learning_style"] == "b"
    assert get_response.json()["activity_intensity"] == "c"

def test_invalid_personality_input(client, test_user):
    data = {
        "openness": "z",  # Invalid value
        "social_energy": "x",  # Invalid value
        "learning_style": "y",  # Invalid value
        "activity_intensity": "w"  # Invalid value
    }
    response = client.post(
        "/api/v1/user-profile/personality",
        json=data,
        headers={"X-User-ID": str(test_user.id)}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # FastAPI should reject invalid values

def test_missing_fields(client, test_user):
    data = {
        "openness": "c"  # Missing other required fields
    }
    response = client.post(
        "/api/v1/user-profile/personality",
        json=data,
        headers={"X-User-ID": str(test_user.id)}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_duplicate_profile(client, test_user, db: Session):
    # Create first profile
    profile = PersonalityProfile(user_id=test_user.id)
    profile.set_personality_data({
        "openness": "c",
        "social_energy": "a",
        "learning_style": "b",
        "activity_intensity": "c"
    })
    db.add(profile)
    db.commit()

    # Try to create second profile for same user via API
    data = {
        "openness": "c",
        "social_energy": "a",
        "learning_style": "b",
        "activity_intensity": "c"
    }
    response = client.post(
        "/api/v1/user-profile/personality",
        json=data,
        headers={"X-User-ID": str(test_user.id)}
    )
    assert response.status_code == status.HTTP_409_CONFLICT  # Should fail due to unique constraint

def test_orm_handling(db: Session, test_user):
    # Test direct ORM handling
    profile = PersonalityProfile(
        user_id=test_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    profile.set_personality_data({
        "openness": "c",
        "social_energy": "a",
        "learning_style": "b",
        "activity_intensity": "c"
    })
    
    db.add(profile)
    db.commit()
    db.refresh(profile)

    # Verify data was saved correctly
    saved_profile = db.query(PersonalityProfile).filter(
        PersonalityProfile.user_id == test_user.id
    ).first()
    assert saved_profile is not None
    assert saved_profile.get_personality_data() == {
        "openness": "c",
        "social_energy": "a",
        "learning_style": "b",
        "activity_intensity": "c"
    } 