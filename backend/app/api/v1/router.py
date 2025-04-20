"""
Main API router.
"""

from fastapi import APIRouter

from app.api.v1 import plaid
from app.api.v1.routes import transactions, personality, session

router = APIRouter(prefix="/api/v1")

# Include Plaid routes
router.include_router(plaid.router)

# Include other routes
router.include_router(transactions.router)
router.include_router(personality.router)
router.include_router(session.router)
