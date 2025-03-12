"""
Main API router.
"""

from fastapi import APIRouter
from app.api.v1 import plaid

router = APIRouter(prefix="/api/v1")

# Include Plaid routes
router.include_router(plaid.router)
