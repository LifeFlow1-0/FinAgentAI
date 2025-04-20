"""
API routes for transaction operations.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.transaction import Transaction as TransactionModel
from app.models.user import User
from app.models.plaid import PlaidItem, PlaidAccount
from app.schemas.transaction import Transaction, TransactionCreate, TransactionUpdate
from app.schemas.enums import TransactionTypeEnum, TransactionStatusEnum

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate, db: Session = Depends(get_db)
):
    """Create a new transaction."""
    # Collect all validation errors
    validation_errors = {}

    # Validate foreign key references
    user = db.query(User).filter(User.id == transaction.user_id).first()
    if not user:
        validation_errors["user_id"] = "User not found"

    plaid_item = db.query(PlaidItem).filter(PlaidItem.id == transaction.plaid_item_id).first()
    if not plaid_item:
        validation_errors["plaid_item_id"] = "Plaid item not found"

    plaid_account = db.query(PlaidAccount).filter(PlaidAccount.id == transaction.plaid_account_id).first()
    if not plaid_account:
        validation_errors["plaid_account_id"] = "Plaid account not found"

    # Validate currency code (simple validation for now)
    valid_currencies = ["USD", "EUR", "GBP", "CAD", "AUD", "JPY"]
    if transaction.currency not in valid_currencies:
        validation_errors["currency"] = "Invalid currency code"

    # If there are any validation errors, raise them all at once
    if validation_errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=validation_errors
        )

    try:
        db_transaction = TransactionModel(**transaction.model_dump(exclude_unset=True))
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return Transaction.model_validate(db_transaction)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[Transaction])
async def list_transactions(
    status: Optional[TransactionStatusEnum] = None,
    type: Optional[TransactionTypeEnum] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all transactions with pagination and filtering."""
    query = db.query(TransactionModel)

    if status:
        query = query.filter(TransactionModel.status == status)
    if type:
        query = query.filter(TransactionModel.type == type)
    if start_date:
        query = query.filter(TransactionModel.transaction_date >= start_date)
    if end_date:
        query = query.filter(TransactionModel.transaction_date <= end_date)

    transactions = query.offset(skip).limit(limit).all()
    return [Transaction.model_validate(t) for t in transactions]


@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get a specific transaction by ID."""
    transaction = (
        db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return Transaction.model_validate(transaction)


@router.put("/{transaction_id}", response_model=Transaction)
async def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db)
):
    """Update a specific transaction."""
    db_transaction = (
        db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    )
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    # Update transaction fields
    update_data = transaction_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaction, field, value)

    try:
        db.commit()
        db.refresh(db_transaction)
        return Transaction.model_validate(db_transaction)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Delete a specific transaction."""
    transaction = (
        db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    try:
        db.delete(transaction)
        db.commit()
        return None
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 