"""
Configuration settings for the LifeFlow application.
"""

from enum import Enum
from pathlib import Path

from pydantic_settings import BaseSettings


class PlaidEnv(str, Enum):
    SANDBOX = "sandbox"
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    # Base Settings
    APP_NAME: str = "LifeFlow"
    DEBUG: bool = True

    # Database Settings
    DATABASE_PATH: str = str(Path(__file__).parent.parent / "data" / "lifeflow.db")

    # API Settings
    API_V1_PREFIX: str = "/api/v1"

    # Plaid Settings
    PLAID_CLIENT_ID: str
    PLAID_SECRET: str
    PLAID_ENV: PlaidEnv = PlaidEnv.SANDBOX
    PLAID_REDIRECT_URI: str = "http://localhost:8000/api/v1/plaid/oauth-redirect"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global Settings Instance
settings = Settings()
