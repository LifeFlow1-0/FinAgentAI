"""
Configuration settings for the LifeFlow application.
"""
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Base Settings
    APP_NAME: str = "LifeFlow"
    DEBUG: bool = True
    
    # Database Settings
    DATABASE_URL: str = f"sqlite:///{Path(__file__).parent.parent}/data/lifeflow.db"
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        case_sensitive = True

# Global Settings Instance
settings = Settings() 