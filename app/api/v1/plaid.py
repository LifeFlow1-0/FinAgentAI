"""
Plaid API routes.
"""
from typing import Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

from app.utils.plaid_client import (
    get_plaid_client,
    create_link_token,
    get_transactions,
    exchange_public_token as exchange_token,
    handle_plaid_error,
    PlaidError
)
from app.database import get_db
from app.models.plaid import PlaidItem, PlaidAccount
from app.schemas.plaid import (
    CreateLinkTokenRequest,
    LinkTokenResponse,
    ExchangeTokenRequest,
    ExchangeTokenResponse,
    TransactionResponse
)

router = APIRouter(prefix="/plaid", tags=["plaid"])

@router.post("/create_link_token", response_model=LinkTokenResponse)
async def create_plaid_link_token(
    request: CreateLinkTokenRequest,
    db: Session = Depends(get_db)
) -> LinkTokenResponse:
    """
    Create a Plaid Link token for initializing Plaid Link.
    """
    try:
        client = get_plaid_client()
        token = create_link_token(client, request.user_id, request.use_redirect)
        return LinkTokenResponse(link_token=token)
    except PlaidError as e:
        raise handle_plaid_error(e)

@router.post("/exchange_public_token", response_model=ExchangeTokenResponse)
async def exchange_public_token(
    request: ExchangeTokenRequest,
    db: Session = Depends(get_db)
) -> ExchangeTokenResponse:
    """
    Exchange public token for access token and store account info.
    """
    try:
        # Check for existing item
        existing_item = db.query(PlaidItem).filter(
            PlaidItem.institution_id == request.institution_id
        ).first()
        if existing_item:
            raise HTTPException(
                status_code=400,
                detail=f"Institution {request.institution_name} already exists"
            )

        client = get_plaid_client()
        # Exchange public token for access token
        access_token, item_id = exchange_token(client, request.public_token)

        # Create Plaid item record
        plaid_item = PlaidItem(
            item_id=item_id,
            access_token=access_token,
            institution_id=request.institution_id,
            institution_name=request.institution_name
        )
        db.add(plaid_item)
        db.flush()  # Get the ID without committing
        
        # Create account records
        for account_data in request.accounts:
            account = PlaidAccount(
                plaid_item_id=plaid_item.id,
                account_id=account_data.id,
                name=account_data.name,
                official_name=account_data.official_name,
                type=account_data.type,
                subtype=account_data.subtype,
                mask=account_data.mask
            )
            db.add(account)
        
        db.commit()
        return ExchangeTokenResponse(status="success", item_id=item_id)
    except HTTPException:
        db.rollback()
        raise
    except PlaidError as e:
        db.rollback()
        raise handle_plaid_error(e)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions/{item_id}", response_model=TransactionResponse)
async def get_plaid_transactions(
    item_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
) -> TransactionResponse:
    """
    Retrieve transactions for a connected Plaid account.
    """
    try:
        # Validate date range
        if start_date and end_date:
            if end_date < start_date:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid date range: end_date must be after start_date"
                )
            
            now = datetime.now()
            if start_date > now or end_date > now:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot request transactions for future dates"
                )

        # Get the Plaid item
        try:
            plaid_item = db.query(PlaidItem).filter(PlaidItem.item_id == item_id).first()
            if not plaid_item:
                raise HTTPException(status_code=404, detail="Plaid item not found")
            
            # Ensure we have the access token before the session might be closed
            access_token = plaid_item.access_token
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )

        client = get_plaid_client()
        transactions_data = get_transactions(
            client,
            access_token,
            start_date,
            end_date
        )
        return TransactionResponse(**transactions_data)
    except PlaidError as e:
        raise handle_plaid_error(e)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) 