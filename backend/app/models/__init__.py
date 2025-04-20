# This file is intentionally empty to make the directory a Python package
from app.database import Base

# Import all models here
from .user import User
from .plaid import PlaidItem, PlaidAccount
from .transaction import Transaction
from .personality import PersonalityProfile
from .onboarding_session import OnboardingSession

__all__ = [
    'Base',
    'User',
    'PlaidItem',
    'PlaidAccount',
    'Transaction',
    'PersonalityProfile',
    'OnboardingSession',
]
