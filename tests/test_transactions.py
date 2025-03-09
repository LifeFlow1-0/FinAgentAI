"""
Tests for transaction endpoints.
"""
import pytest
from datetime import datetime

def test_create_transaction(client):
    """Test creating a new transaction."""
    transaction_data = {
        "amount": 1000.00,
        "type": "income",
        "category": "salary",
        "description": "Monthly salary",
        "date": datetime.utcnow().isoformat()
    }
    
    response = client.post("/api/v1/transactions/", json=transaction_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["amount"] == transaction_data["amount"]
    assert data["type"] == transaction_data["type"]
    assert data["category"] == transaction_data["category"]
    assert data["description"] == transaction_data["description"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_list_transactions(client):
    """Test listing transactions with pagination."""
    # Create two transactions
    for i in range(2):
        transaction_data = {
            "amount": 1000.00 + i,
            "type": "income",
            "category": "salary",
            "description": f"Transaction {i}",
            "date": datetime.utcnow().isoformat()
        }
        client.post("/api/v1/transactions/", json=transaction_data)
    
    # Test default pagination
    response = client.get("/api/v1/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Test with limit
    response = client.get("/api/v1/transactions/?limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_get_transaction(client):
    """Test getting a single transaction."""
    # Create a transaction
    transaction_data = {
        "amount": 1000.00,
        "type": "income",
        "category": "salary",
        "description": "Test transaction",
        "date": datetime.utcnow().isoformat()
    }
    create_response = client.post("/api/v1/transactions/", json=transaction_data)
    created_transaction = create_response.json()
    
    # Get the transaction
    response = client.get(f"/api/v1/transactions/{created_transaction['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_transaction["id"]
    assert data["amount"] == transaction_data["amount"]

def test_update_transaction(client):
    """Test updating a transaction."""
    # Create a transaction
    transaction_data = {
        "amount": 1000.00,
        "type": "income",
        "category": "salary",
        "description": "Original description",
        "date": datetime.utcnow().isoformat()
    }
    create_response = client.post("/api/v1/transactions/", json=transaction_data)
    created_transaction = create_response.json()
    
    # Update the transaction
    update_data = dict(transaction_data)
    update_data["description"] = "Updated description"
    response = client.put(
        f"/api/v1/transactions/{created_transaction['id']}", 
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated description"
    assert data["updated_at"] != data["created_at"]

def test_delete_transaction(client):
    """Test deleting a transaction."""
    # Create a transaction
    transaction_data = {
        "amount": 1000.00,
        "type": "income",
        "category": "salary",
        "description": "To be deleted",
        "date": datetime.utcnow().isoformat()
    }
    create_response = client.post("/api/v1/transactions/", json=transaction_data)
    created_transaction = create_response.json()
    
    # Delete the transaction
    response = client.delete(f"/api/v1/transactions/{created_transaction['id']}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/transactions/{created_transaction['id']}")
    assert get_response.status_code == 404

def test_create_invalid_transaction(client):
    """Test creating a transaction with invalid data."""
    # Test with negative amount
    transaction_data = {
        "amount": -100.00,
        "type": "income",
        "category": "salary",
        "description": "Invalid amount",
        "date": datetime.utcnow().isoformat()
    }
    response = client.post("/api/v1/transactions/", json=transaction_data)
    assert response.status_code == 422  # Validation error

def test_get_nonexistent_transaction(client):
    """Test getting a transaction that doesn't exist."""
    response = client.get("/api/v1/transactions/999")
    assert response.status_code == 404 