"""
API routes for transaction operations.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.transaction import Transaction as TransactionModel
from app.schemas.transaction import Transaction, TransactionCreate

router = APIRouter(prefix="/api/v1/transactions", tags=["transactions"])


@router.post("/", response_model=Transaction)
async def create_transaction(
    transaction: TransactionCreate, db: Session = Depends(get_db)
):
    """Create a new transaction."""
    db_transaction = TransactionModel(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.get("/", response_model=List[Transaction])
async def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    db: Session = Depends(get_db),
):
    """List all transactions with pagination."""
    transactions = db.query(TransactionModel).offset(skip).limit(limit).all()
    return transactions


@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get a specific transaction by ID."""
    transaction = (
        db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    )
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=Transaction)
async def update_transaction(
    transaction_id: int,
    transaction_update: TransactionCreate,
    db: Session = Depends(get_db),
):
    """Update a specific transaction."""
    db_transaction = (
        db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    )
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in transaction_update.model_dump().items():
        setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.delete("/{transaction_id}", response_model=Transaction)
async def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Delete a specific transaction."""
    transaction = (
        db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    )
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()
    return transaction
