"""
Tests for transaction endpoints.
"""
import pytest
from datetime import datetime, timedelta
from fastapi import status
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.enums import TransactionTypeEnum, TransactionStatusEnum


def test_create_transaction(client, test_transaction):
    response = client.post("/api/v1/transactions/", json=test_transaction)
    print("Response:", response.json())
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["amount"] == test_transaction["amount"]
    assert data["type"] == test_transaction["type"]
    assert data["status"] == test_transaction["status"]


def test_list_transactions(client, test_user, test_plaid_account):
    """Test listing all transactions."""
    # Create a few transactions
    for i in range(3):
        transaction_data = {
            "amount": 1000.00 + i,
            "currency": "USD",
            "type": TransactionTypeEnum.INCOME,
            "category": "salary",
            "merchant_name": f"ACME Corp {i}",
            "description": f"Test transaction {i}",
            "transaction_date": datetime.utcnow().isoformat(),
            "posted_date": datetime.utcnow().isoformat(),
            "status": TransactionStatusEnum.POSTED,
            "user_id": test_user.id,
            "plaid_item_id": test_plaid_account.plaid_item_id,
            "plaid_account_id": test_plaid_account.id
        }
        client.post("/api/v1/transactions/", json=transaction_data)
    
    response = client.get("/api/v1/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_get_transaction(client, test_user, test_plaid_account):
    """Test getting a single transaction."""
    transaction_data = {
        "amount": 1000.00,
        "currency": "USD",
        "type": TransactionTypeEnum.INCOME,
        "category": "salary",
        "merchant_name": "ACME Corp",
        "description": "Test transaction",
        "transaction_date": datetime.utcnow().isoformat(),
        "posted_date": datetime.utcnow().isoformat(),
        "status": TransactionStatusEnum.POSTED,
        "user_id": test_user.id,
        "plaid_item_id": test_plaid_account.plaid_item_id,
        "plaid_account_id": test_plaid_account.id
    }
    create_response = client.post("/api/v1/transactions/", json=transaction_data)
    created_transaction = create_response.json()
    
    response = client.get(f"/api/v1/transactions/{created_transaction['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_transaction["id"]
    assert data["amount"] == transaction_data["amount"]
    assert data["merchant_name"] == transaction_data["merchant_name"]


def test_update_transaction(client, test_user, test_plaid_account):
    """Test updating a transaction."""
    transaction_data = {
        "amount": 1000.00,
        "currency": "USD",
        "type": TransactionTypeEnum.INCOME,
        "category": "salary",
        "merchant_name": "ACME Corp",
        "description": "Original description",
        "transaction_date": datetime.utcnow().isoformat(),
        "posted_date": datetime.utcnow().isoformat(),
        "status": TransactionStatusEnum.PENDING,
        "user_id": test_user.id,
        "plaid_item_id": test_plaid_account.plaid_item_id,
        "plaid_account_id": test_plaid_account.id
    }
    create_response = client.post("/api/v1/transactions/", json=transaction_data)
    created_transaction = create_response.json()
    
    # Update the transaction
    update_data = dict(transaction_data)
    update_data["description"] = "Updated description"
    update_data["status"] = TransactionStatusEnum.POSTED
    response = client.put(
        f"/api/v1/transactions/{created_transaction['id']}", 
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated description"
    assert data["status"] == TransactionStatusEnum.POSTED
    assert data["updated_at"] != data["created_at"]


def test_delete_transaction(client, test_user, test_plaid_account):
    """Test deleting a transaction."""
    transaction_data = {
        "amount": 1000.00,
        "currency": "USD",
        "type": TransactionTypeEnum.INCOME,
        "category": "salary",
        "merchant_name": "ACME Corp",
        "description": "To be deleted",
        "transaction_date": datetime.utcnow().isoformat(),
        "posted_date": datetime.utcnow().isoformat(),
        "status": TransactionStatusEnum.POSTED,
        "user_id": test_user.id,
        "plaid_item_id": test_plaid_account.plaid_item_id,
        "plaid_account_id": test_plaid_account.id
    }
    create_response = client.post("/api/v1/transactions/", json=transaction_data)
    created_transaction = create_response.json()
    
    response = client.delete(f"/api/v1/transactions/{created_transaction['id']}")
    assert response.status_code == 200
    
    get_response = client.get(f"/api/v1/transactions/{created_transaction['id']}")
    assert get_response.status_code == 404


def test_create_invalid_transaction(client, test_user, test_plaid_account):
    """Test creating a transaction with invalid data."""
    # Test with negative amount
    transaction_data = {
        "amount": -100.00,
        "currency": "USD",
        "type": TransactionTypeEnum.INCOME,
        "category": "salary",
        "merchant_name": "ACME Corp",
        "description": "Invalid amount",
        "transaction_date": datetime.utcnow().isoformat(),
        "posted_date": datetime.utcnow().isoformat(),
        "status": TransactionStatusEnum.POSTED,
        "user_id": test_user.id,
        "plaid_item_id": test_plaid_account.plaid_item_id,
        "plaid_account_id": test_plaid_account.id
    }
    response = client.post("/api/v1/transactions/", json=transaction_data)
    assert response.status_code == 422  # Validation error


def test_create_transaction_invalid_references(client, test_transaction):
    test_transaction["plaid_item_id"] = 999  # Non-existent ID
    test_transaction["plaid_account_id"] = 999  # Non-existent ID
    response = client.post("/api/v1/transactions/", json=test_transaction)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "plaid_item_id" in str(data)
    assert "plaid_account_id" in str(data)


def test_create_transaction_invalid_currency(client, test_transaction):
    test_transaction["currency"] = "INVALID"
    response = client.post("/api/v1/transactions/", json=test_transaction)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_transaction_invalid_dates(client, test_user, test_plaid_account):
    """Test creating a transaction with invalid dates."""
    transaction_data = {
        "amount": 1000.00,
        "currency": "USD",
        "type": TransactionTypeEnum.INCOME,
        "category": "salary",
        "merchant_name": "ACME Corp",
        "description": "Invalid dates",
        "transaction_date": "invalid-date",  # Invalid date format
        "posted_date": "invalid-date",  # Invalid date format
        "status": TransactionStatusEnum.POSTED,
        "user_id": test_user.id,
        "plaid_item_id": test_plaid_account.plaid_item_id,
        "plaid_account_id": test_plaid_account.id
    }
    response = client.post("/api/v1/transactions/", json=transaction_data)
    assert response.status_code == 422  # Validation error


def test_get_transactions_by_status(client, db: Session, test_user, test_plaid_account):
    # Create test transactions with different statuses
    transactions = [
        Transaction(
            amount=100.0,
            currency="USD",
            type=TransactionTypeEnum.EXPENSE,
            status=TransactionStatusEnum.PENDING,
            category="groceries",
            transaction_date=datetime.utcnow(),
            posted_date=datetime.utcnow(),
            user_id=test_user.id,
            plaid_item_id=test_plaid_account.plaid_item_id,
            plaid_account_id=test_plaid_account.id
        ),
        Transaction(
            amount=200.0,
            currency="USD",
            type=TransactionTypeEnum.INCOME,
            status=TransactionStatusEnum.POSTED,
            category="salary",
            transaction_date=datetime.utcnow(),
            posted_date=datetime.utcnow(),
            user_id=test_user.id,
            plaid_item_id=test_plaid_account.plaid_item_id,
            plaid_account_id=test_plaid_account.id
        )
    ]
    for t in transactions:
        db.add(t)
    db.commit()

    # Test filtering by status
    response = client.get("/api/v1/transactions/?status=pending")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert all(t["status"] == "pending" for t in data)


def test_get_transactions_by_date_range(client, db: Session, test_user, test_plaid_account):
    # Create test transactions with different dates
    base_date = datetime.utcnow()
    transactions = [
        Transaction(
            amount=100.0,
            currency="USD",
            type=TransactionTypeEnum.EXPENSE,
            status=TransactionStatusEnum.PENDING,
            category="groceries",
            transaction_date=base_date - timedelta(days=5),
            posted_date=base_date - timedelta(days=5),
            user_id=test_user.id,
            plaid_item_id=test_plaid_account.plaid_item_id,
            plaid_account_id=test_plaid_account.id
        ),
        Transaction(
            amount=200.0,
            currency="USD",
            type=TransactionTypeEnum.INCOME,
            status=TransactionStatusEnum.POSTED,
            category="salary",
            transaction_date=base_date,
            posted_date=base_date,
            user_id=test_user.id,
            plaid_item_id=test_plaid_account.plaid_item_id,
            plaid_account_id=test_plaid_account.id
        ),
        Transaction(
            amount=300.0,
            currency="USD",
            type=TransactionTypeEnum.TRANSFER,
            status=TransactionStatusEnum.POSTED,
            category="transfer",
            transaction_date=base_date + timedelta(days=5),
            posted_date=base_date + timedelta(days=5),
            user_id=test_user.id,
            plaid_item_id=test_plaid_account.plaid_item_id,
            plaid_account_id=test_plaid_account.id
        )
    ]
    for t in transactions:
        db.add(t)
    db.commit()

    # Test filtering by date range
    start_date = (base_date - timedelta(days=1)).isoformat()
    end_date = (base_date + timedelta(days=1)).isoformat()
    response = client.get(f"/api/v1/transactions/?start_date={start_date}&end_date={end_date}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1  # Only the transaction with base_date should be included 