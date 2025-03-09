"""
Tests for Plaid API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch, Mock
from plaid.model.plaid_error import PlaidError as PlaidApiError
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

from app.models.plaid import PlaidItem, PlaidAccount
from app.schemas.plaid import PlaidAccountRequest
from app.utils.plaid_client import PlaidError

@patch("app.api.v1.plaid.get_plaid_client")
def test_create_link_token(mock_get_client, client: TestClient, mock_plaid_client):
    """Test creating a Plaid Link token."""
    mock_get_client.return_value = mock_plaid_client
    response = client.post(
        "/api/v1/plaid/create_link_token",
        json={
            "user_id": "test_user",
            "use_redirect": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["link_token"] == "test_link_token"

@patch("app.api.v1.plaid.get_plaid_client")
def test_create_link_token_error(mock_get_client, client: TestClient, mock_plaid_client):
    """Test error handling when creating a link token fails."""
    mock_get_client.return_value = mock_plaid_client
    mock_plaid_client.link_token_create.side_effect = Exception("Failed to create link token")
    
    response = client.post(
        "/api/v1/plaid/create_link_token",
        json={
            "user_id": "test_user",
            "use_redirect": True
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "message" in data["detail"]
    assert "Failed to create link token" in str(data["detail"])

@patch("app.api.v1.plaid.get_plaid_client")
def test_exchange_public_token(mock_get_client, client: TestClient, db: Session, mock_plaid_client):
    """Test exchanging a public token for access token."""
    mock_get_client.return_value = mock_plaid_client
    # Test data
    test_accounts = [
        PlaidAccountRequest(
            id="test_account_1",
            name="Test Checking",
            type="depository",
            subtype="checking"
        )
    ]
    
    response = client.post(
        "/api/v1/plaid/exchange_public_token",
        json={
            "public_token": "test_public_token",
            "institution_id": "ins_123",
            "institution_name": "Test Bank",
            "accounts": [account.model_dump() for account in test_accounts]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["item_id"] == "test_item_id"

    # Verify database records
    plaid_item = db.query(PlaidItem).filter(
        PlaidItem.institution_id == "ins_123"
    ).first()
    assert plaid_item is not None
    assert plaid_item.institution_name == "Test Bank"
    assert plaid_item.access_token == "test_access_token"

    plaid_account = db.query(PlaidAccount).filter(
        PlaidAccount.plaid_item_id == plaid_item.id
    ).first()
    assert plaid_account is not None
    assert plaid_account.name == "Test Checking"
    assert plaid_account.type == "depository"

@patch("app.api.v1.plaid.get_plaid_client")
def test_exchange_public_token_error(mock_get_client, client: TestClient, mock_plaid_client):
    """Test error handling when exchanging public token fails."""
    mock_get_client.return_value = mock_plaid_client
    mock_plaid_client.item_public_token_exchange.side_effect = PlaidError(
        "Failed to exchange public token"
    )
    
    response = client.post(
        "/api/v1/plaid/exchange_public_token",
        json={
            "public_token": "invalid_token",
            "institution_id": "ins_123",
            "institution_name": "Test Bank",
            "accounts": []
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "message" in data["detail"]
    assert "Failed to exchange public token" in str(data["detail"])

def test_exchange_public_token_invalid_request(client: TestClient):
    """Test validation error handling for invalid request data."""
    response = client.post(
        "/api/v1/plaid/exchange_public_token",
        json={
            # Missing required fields
            "public_token": "",
            "institution_name": "Test Bank"
        }
    )
    assert response.status_code == 422  # Validation error
    data = response.json()
    assert "detail" in data

@patch("app.api.v1.plaid.get_plaid_client")
def test_get_transactions(mock_get_client, client: TestClient, db: Session, mock_plaid_client):
    """Test retrieving transactions."""
    mock_get_client.return_value = mock_plaid_client
    # Create a test Plaid item first
    plaid_item = PlaidItem(
        item_id="test_item_id",
        access_token="test_access_token",
        institution_id="ins_123",
        institution_name="Test Bank"
    )
    db.add(plaid_item)
    db.commit()

    response = client.get(f"/api/v1/plaid/transactions/{plaid_item.item_id}")
    assert response.status_code == 200
    data = response.json()
    assert "accounts" in data
    assert "transactions" in data

@patch("app.api.v1.plaid.get_plaid_client")
def test_get_transactions_error(mock_get_client, client: TestClient, db: Session, mock_plaid_client):
    """Test error handling when retrieving transactions fails."""
    mock_get_client.return_value = mock_plaid_client
    # Create a test Plaid item first
    plaid_item = PlaidItem(
        item_id="test_item_id",
        access_token="test_access_token",
        institution_id="ins_123",
        institution_name="Test Bank"
    )
    db.add(plaid_item)
    db.commit()

    mock_plaid_client.transactions_get.side_effect = Exception("Failed to retrieve transactions")

    response = client.get(f"/api/v1/plaid/transactions/{plaid_item.item_id}")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "message" in data["detail"]
    assert "Failed to retrieve transactions" in str(data["detail"])

def test_get_transactions_not_found(client: TestClient):
    """Test retrieving transactions for non-existent item."""
    response = client.get("/api/v1/plaid/transactions/non_existent_id")
    assert response.status_code == 404

@patch("app.api.v1.plaid.get_plaid_client")
def test_get_transactions_invalid_dates(mock_get_client, client: TestClient, db: Session, mock_plaid_client):
    """Test error handling for invalid date parameters."""
    mock_get_client.return_value = mock_plaid_client
    # Create a test Plaid item first
    plaid_item = PlaidItem(
        item_id="test_item_id",
        access_token="test_access_token",
        institution_id="ins_123",
        institution_name="Test Bank"
    )
    db.add(plaid_item)
    db.commit()

    response = client.get(
        f"/api/v1/plaid/transactions/{plaid_item.item_id}",
        params={
            "start_date": "invalid_date",
            "end_date": "2024-03-20"
        }
    )
    assert response.status_code == 422  # Validation error
    data = response.json()
    assert "detail" in data 

@patch("app.api.v1.plaid.get_plaid_client")
def test_create_link_token_missing_user_id(mock_get_client, client: TestClient):
    """Test error handling when user_id is missing."""
    response = client.post(
        "/api/v1/plaid/create_link_token",
        json={
            "use_redirect": True
        }
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("user_id" in error["loc"] for error in data["detail"])

@patch("app.api.v1.plaid.get_plaid_client")
def test_exchange_public_token_duplicate_item(mock_get_client, client: TestClient, db: Session, mock_plaid_client):
    """Test error handling when trying to add a duplicate Plaid item."""
    mock_get_client.return_value = mock_plaid_client
    
    # Create existing Plaid item
    existing_item = PlaidItem(
        item_id="test_item_id",
        access_token="test_access_token",
        institution_id="ins_123",
        institution_name="Test Bank"
    )
    db.add(existing_item)
    db.commit()
    
    # Try to add the same item again
    response = client.post(
        "/api/v1/plaid/exchange_public_token",
        json={
            "public_token": "test_public_token",
            "institution_id": "ins_123",
            "institution_name": "Test Bank",
            "accounts": []
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already exists" in str(data["detail"])

@patch("app.api.v1.plaid.get_plaid_client")
def test_get_transactions_with_date_range(mock_get_client, client: TestClient, db: Session, mock_plaid_client):
    """Test retrieving transactions with a specific date range."""
    mock_get_client.return_value = mock_plaid_client
    
    # Create a test Plaid item
    plaid_item = PlaidItem(
        item_id="test_item_id",
        access_token="test_access_token",
        institution_id="ins_123",
        institution_name="Test Bank"
    )
    db.add(plaid_item)
    db.commit()

    # Set up date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    response = client.get(
        f"/api/v1/plaid/transactions/{plaid_item.item_id}",
        params={
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "accounts" in data
    assert "transactions" in data

@patch("app.api.v1.plaid.get_plaid_client")
def test_get_transactions_future_dates(mock_get_client, client: TestClient, db: Session, mock_plaid_client):
    """Test error handling when requesting transactions with future dates."""
    mock_get_client.return_value = mock_plaid_client
    
    # Create a test Plaid item
    plaid_item = PlaidItem(
        item_id="test_item_id",
        access_token="test_access_token",
        institution_id="ins_123",
        institution_name="Test Bank"
    )
    db.add(plaid_item)
    db.commit()

    # Set up future date range
    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(days=30)

    response = client.get(
        f"/api/v1/plaid/transactions/{plaid_item.item_id}",
        params={
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "future dates" in str(data["detail"]).lower()

@patch("app.api.v1.plaid.get_plaid_client")
def test_get_transactions_invalid_date_range(mock_get_client, client: TestClient, db: Session, mock_plaid_client):
    """Test error handling when end_date is before start_date."""
    mock_get_client.return_value = mock_plaid_client
    
    # Create a test Plaid item
    plaid_item = PlaidItem(
        item_id="test_item_id",
        access_token="test_access_token",
        institution_id="ins_123",
        institution_name="Test Bank"
    )
    db.add(plaid_item)
    db.commit()

    # Set up invalid date range
    start_date = datetime.now()
    end_date = start_date - timedelta(days=1)

    response = client.get(
        f"/api/v1/plaid/transactions/{plaid_item.item_id}",
        params={
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "invalid date range" in str(data["detail"]).lower()

@patch("app.api.v1.plaid.get_plaid_client")
def test_get_transactions_db_error(mock_get_client, client: TestClient, db: Session, mock_plaid_client):
    """Test error handling when database query fails."""
    mock_get_client.return_value = mock_plaid_client
    
    # Create a test Plaid item
    plaid_item = PlaidItem(
        item_id="test_item_id",
        access_token="test_access_token",
        institution_id="ins_123",
        institution_name="Test Bank"
    )
    db.add(plaid_item)
    db.commit()
    
    # Store the item_id before closing the session
    item_id = plaid_item.item_id
    
    # Mock the database query to raise an error
    with patch("sqlalchemy.orm.Session.query") as mock_query:
        mock_query.side_effect = SQLAlchemyError("Database connection error")
        
        response = client.get(f"/api/v1/plaid/transactions/{item_id}")
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "database error" in str(data["detail"]).lower()

@patch("app.api.v1.plaid.get_plaid_client")
def test_exchange_public_token_invalid_account_type(mock_get_client, client: TestClient, mock_plaid_client):
    """Test error handling when account type is invalid."""
    mock_get_client.return_value = mock_plaid_client
    
    response = client.post(
        "/api/v1/plaid/exchange_public_token",
        json={
            "public_token": "test_public_token",
            "institution_id": "ins_123",
            "institution_name": "Test Bank",
            "accounts": [{
                "id": "test_account_1",
                "name": "Test Account",
                "type": "invalid_type",  # Invalid account type
                "subtype": None
            }]
        }
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("type" in error["loc"] for error in data["detail"]) 