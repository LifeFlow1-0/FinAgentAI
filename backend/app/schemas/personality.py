"""
Pydantic schemas for personality data validation.
"""

from typing import Literal
from pydantic import BaseModel, ConfigDict, constr
from datetime import datetime

# Valid values for each personality trait
OpennessType = Literal["a", "b", "c"]  # a=Conservative, b=Moderate, c=Explorer
SocialEnergyType = Literal["a", "b", "c"]  # a=Introvert, b=Ambivert, c=Extrovert
LearningStyleType = Literal["a", "b", "c"]  # a=Visual, b=Mixed, c=Auditory
ActivityIntensityType = Literal["a", "b", "c"]  # a=Calm, b=Balanced, c=Dynamic

class PersonalityProfileBase(BaseModel):
    """Base schema for personality profile data."""
    openness: OpennessType
    social_energy: SocialEnergyType
    learning_style: LearningStyleType
    activity_intensity: ActivityIntensityType

class PersonalityProfileCreate(PersonalityProfileBase):
    """Schema for creating a new personality profile."""
    pass

class PersonalityProfileResponse(PersonalityProfileBase):
    """Schema for personality profile responses."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 