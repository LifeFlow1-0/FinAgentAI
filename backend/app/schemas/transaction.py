"""
Pydantic schemas for transaction validation.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, field_validator, ConfigDict

from app.schemas.enums import TransactionTypeEnum, TransactionStatusEnum


class TransactionBase(BaseModel):
    amount: Decimal
    currency: str
    type: TransactionTypeEnum
    status: TransactionStatusEnum
    category: str
    merchant_name: Optional[str] = None
    description: Optional[str] = None
    transaction_date: datetime
    posted_date: datetime
    plaid_item_id: int
    plaid_account_id: int

    @field_validator("type", "status", mode="before")
    def convert_to_enum(cls, value):
        if isinstance(value, str):
            value = value.lower()
        return value

    @field_validator("amount")
    def validate_amount(cls, value):
        if value < 0:
            raise ValueError("Amount cannot be negative")
        return value

    model_config = ConfigDict(from_attributes=True, json_encoders={Decimal: lambda v: float(v)})


class TransactionCreate(TransactionBase):
    user_id: int


class TransactionUpdate(TransactionBase):
    user_id: int


class Transaction(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
