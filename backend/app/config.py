"""
Configuration settings for the LifeFlow application.
"""

from enum import Enum
from pathlib import Path
import os
from cryptography.fernet import Fernet

from pydantic_settings import BaseSettings


class PlaidEnv(str, Enum):
    SANDBOX = "sandbox"
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Environment(str, Enum):
    DEV = "development"
    GAMMA = "gamma"
    PROD = "production"
    TEST = "test"


class Settings(BaseSettings):
    # Base Settings
    APP_NAME: str = "LifeFlow"
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.DEV

    # Database Settings
    # For dev, we use the project root directory
    # For gamma/prod, we use a mounted volume at /app/data
    DATABASE_PATH: str = str(Path(__file__).parent.parent / "lifeflow.db")

    # API Settings
    API_V1_PREFIX: str = "/api/v1"

    # Security Settings
    ENCRYPTION_KEY: str = Fernet.generate_key().decode()  # Default to a new key if not provided

    # Plaid Settings
    PLAID_CLIENT_ID: str = "test_client_id"  # Default for testing
    PLAID_SECRET: str = "test_secret"  # Default for testing
    PLAID_ENV: PlaidEnv = PlaidEnv.SANDBOX
    PLAID_REDIRECT_URI: str = "http://localhost:8000/api/v1/plaid/oauth-redirect"

    def __init__(self, **kwargs):
        # Set env_file from ENV_FILE environment variable if provided
        env_file = os.getenv("ENV_FILE")
        if env_file:
            self.model_config["env_file"] = env_file
        
        # Otherwise, load from the default .env file
        super().__init__(**kwargs)
        
        # Set database path based on environment if not explicitly provided
        if 'DATABASE_PATH' not in kwargs and self.ENVIRONMENT in [Environment.GAMMA, Environment.PROD]:
            # For gamma and prod, use a mounted volume
            database_name = f"lifeflow_{self.ENVIRONMENT}.db"
            self.DATABASE_PATH = str(Path("/app/data") / database_name)
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True, 
        "extra": "allow"
    }


# Global Settings Instance
settings = Settings()
