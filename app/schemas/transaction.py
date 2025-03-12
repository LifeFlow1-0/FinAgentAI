"""
Pydantic schemas for transaction validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount")
    type: str = Field(..., description="Type of transaction")
    category: str = Field(..., description="Transaction category")
    description: Optional[str] = Field(
        None, description="Optional transaction description"
    )
    date: datetime = Field(
        default_factory=datetime.utcnow, description="Transaction date"
    )


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
