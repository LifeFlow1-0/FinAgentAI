"""
Tests for personality profile API endpoints.
"""

import pytest
from fastapi import status
from sqlalchemy.orm import Session

# Import models within test functions to avoid circular imports

def test_create_personality_profile(client, test_user):
    """Test creating a personality profile."""
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
    
    # First assert the initial response
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == "success"
    assert "id" in response.json()
    
    # Now fetch the created profile and assert its contents
    get_response = client.get(f"/api/v1/user-profile/personality/{test_user.id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["user_id"] == test_user.id
    assert get_response.json()["openness"] == "c"
    assert get_response.json()["social_energy"] == "a"
    assert get_response.json()["learning_style"] == "b"
    assert get_response.json()["activity_intensity"] == "c"

def test_create_personality_profile_invalid_user(client):
    """Test creating a profile for non-existent user."""
    data = {
        "openness": "c",
        "social_energy": "a",
        "learning_style": "b",
        "activity_intensity": "c"
    }
    
    response = client.post(
        "/api/v1/user-profile/personality",
        json=data,
        headers={"X-User-ID": "999"}
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "User not found" in response.json()["detail"]

def test_create_duplicate_personality_profile(client, test_user, db: Session):
    """Test creating a profile when one already exists."""
    # Import here to avoid circular imports
    from app.models.personality import PersonalityProfile
    
    # Create initial profile
    profile = PersonalityProfile(user_id=test_user.id)
    profile.set_personality_data({
        "openness": "a",
        "social_energy": "b",
        "learning_style": "c",
        "activity_intensity": "a"
    })
    db.add(profile)
    db.commit()
    
    # Try to create another profile
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
    
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response.json()["detail"]

def test_create_personality_profile_invalid_data(client, test_user):
    """Test creating a profile with invalid data."""
    data = {
        "openness": "invalid",
        "social_energy": "a",
        "learning_style": "b",
        "activity_intensity": "c"
    }
    
    response = client.post(
        "/api/v1/user-profile/personality",
        json=data,
        headers={"X-User-ID": str(test_user.id)}
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_personality_profile(client, test_user, db: Session):
    """Test retrieving a personality profile."""
    # Import here to avoid circular imports
    from app.models.personality import PersonalityProfile
    
    # Create profile
    profile = PersonalityProfile(user_id=test_user.id)
    profile.set_personality_data({
        "openness": "a",
        "social_energy": "b",
        "learning_style": "c",
        "activity_intensity": "a"
    })
    db.add(profile)
    db.commit()
    
    response = client.get(f"/api/v1/user-profile/personality/{test_user.id}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["user_id"] == test_user.id
    assert response.json()["openness"] == "a"
    assert response.json()["social_energy"] == "b"
    assert response.json()["learning_style"] == "c"
    assert response.json()["activity_intensity"] == "a"

def test_get_nonexistent_personality_profile(client):
    """Test retrieving a non-existent profile."""
    response = client.get("/api/v1/user-profile/personality/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"] 