"""
Pydantic models for Plaid API.
"""

from datetime import datetime
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class LinkTokenResponse(BaseModel):
    """Response model for link token creation."""

    model_config = ConfigDict(from_attributes=True)
    link_token: str


class PlaidAccountRequest(BaseModel):
    """Model for Plaid account data."""

    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    official_name: Optional[str] = None
    type: Literal["depository", "credit", "loan", "investment", "other"]
    subtype: Optional[str] = None
    mask: Optional[str] = None


class ExchangeTokenRequest(BaseModel):
    """Request model for exchanging public token."""

    model_config = ConfigDict(from_attributes=True)
    public_token: str
    institution_id: str
    institution_name: str
    accounts: List[PlaidAccountRequest]


class ExchangeTokenResponse(BaseModel):
    """Response model for token exchange."""

    model_config = ConfigDict(from_attributes=True)
    status: str
    item_id: str


class TransactionResponse(BaseModel):
    """Response model for transactions."""

    model_config = ConfigDict(from_attributes=True)
    accounts: List[Dict]
    transactions: List[Dict]


class CreateLinkTokenRequest(BaseModel):
    """Request model for creating link token."""

    model_config = ConfigDict(from_attributes=True)
    user_id: str
    use_redirect: bool = True
