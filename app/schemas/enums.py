"""
Enum definitions for the application.
"""

from enum import Enum


class CaseInsensitiveEnum(str, Enum):
    """Base class for case-insensitive enums."""
    @classmethod
    def _missing_(cls, value):
        if not isinstance(value, str):
            return None
        value = value.lower()
        for member in cls:
            if member.value.lower() == value:
                return member
        return None


class TransactionTypeEnum(CaseInsensitiveEnum):
    """Case-insensitive transaction type enum."""
    INCOME = "income"
    EXPENSE = "expense"
    INVESTMENT = "investment"
    TRANSFER = "transfer"


class TransactionStatusEnum(CaseInsensitiveEnum):
    """Case-insensitive transaction status enum."""
    PENDING = "pending"
    POSTED = "posted" 