"""
SQLAlchemy model for storing user personality data.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.core.security import encrypt_data, decrypt_data

class PersonalityProfile(Base):
    """Model for storing user personality profile data."""
    
    __tablename__ = "personality_profiles"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key to User
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Encrypted Personality Data
    openness = Column(String, nullable=False)  # Encrypted
    social_energy = Column(String, nullable=False)  # Encrypted
    learning_style = Column(String, nullable=False)  # Encrypted
    activity_intensity = Column(String, nullable=False)  # Encrypted
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="personality_profile")

    def set_personality_data(self, data: dict):
        """Encrypt and set personality data."""
        self.openness = encrypt_data(data['openness'])
        self.social_energy = encrypt_data(data['social_energy'])
        self.learning_style = encrypt_data(data['learning_style'])
        self.activity_intensity = encrypt_data(data['activity_intensity'])

    def get_personality_data(self) -> dict:
        """Decrypt and return personality data."""
        return {
            'openness': decrypt_data(self.openness),
            'social_energy': decrypt_data(self.social_energy),
            'learning_style': decrypt_data(self.learning_style),
            'activity_intensity': decrypt_data(self.activity_intensity)
        } 