"""
Transaction model for the database.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Index, Enum
from sqlalchemy.orm import relationship

from app.database import Base
from app.schemas.enums import TransactionTypeEnum, TransactionStatusEnum


class Transaction(Base):
    """Transaction model for storing financial transactions."""

    __tablename__ = "transactions"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys and References
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plaid_item_id = Column(Integer, ForeignKey("plaid_items.id"), nullable=False)
    plaid_account_id = Column(Integer, ForeignKey("plaid_accounts.id"), nullable=False)
    
    # Transaction Details
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False, default="USD")
    type = Column(Enum(TransactionTypeEnum), nullable=False)
    category = Column(String, nullable=False)
    merchant_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    
    # Status and Dates
    status = Column(Enum(TransactionStatusEnum), nullable=False, default=TransactionStatusEnum.PENDING)
    transaction_date = Column(DateTime, nullable=False)
    posted_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="transactions")
    plaid_item = relationship("PlaidItem", back_populates="transactions")
    plaid_account = relationship("PlaidAccount", back_populates="transactions")

    # Indexes for performance
    __table_args__ = (
        Index('ix_transactions_user_id', 'user_id'),
        Index('ix_transactions_plaid_account_id', 'plaid_account_id'),
        Index('ix_transactions_transaction_date', 'transaction_date'),
        Index('ix_transactions_status', 'status'),
    )
