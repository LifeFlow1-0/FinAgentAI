"""
Models for Plaid data.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class PlaidItem(Base):
    """Model for storing Plaid items (connected financial institutions)."""
    __tablename__ = "plaid_items"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String, unique=True, index=True)
    access_token = Column(String, unique=True)
    institution_id = Column(String)
    institution_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    accounts = relationship("PlaidAccount", back_populates="item")

class PlaidAccount(Base):
    """Model for storing Plaid accounts within items."""
    __tablename__ = "plaid_accounts"

    id = Column(Integer, primary_key=True, index=True)
    plaid_item_id = Column(Integer, ForeignKey("plaid_items.id"))
    account_id = Column(String, unique=True, index=True)
    name = Column(String)
    official_name = Column(String, nullable=True)
    type = Column(String)
    subtype = Column(String, nullable=True)
    mask = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    item = relationship("PlaidItem", back_populates="accounts") 