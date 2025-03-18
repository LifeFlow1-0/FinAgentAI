"""
API Tests for Transaction Endpoints with curl equivalents.

Each test includes the equivalent curl command in its docstring for easy manual testing
and documentation purposes.
"""
import pytest
from datetime import datetime
from fastapi import status


def test_create_transaction_api(client, test_transaction):
    """Test creating a new transaction.
    
    Equivalent curl command:
    ```bash
    curl -X POST http://localhost:8000/api/v1/transactions/ \
         -H "Content-Type: application/json" \
         -d '{
             "amount": 100.0,
             "currency": "USD",
             "type": "expense",
             "status": "pending",
             "category": "groceries",
             "description": "Test transaction",
             "transaction_date": "2024-03-14T00:00:00Z",
             "posted_date": "2024-03-14T00:00:00Z",
             "plaid_item_id": 1,
             "plaid_account_id": 1,
             "user_id": 1
         }'
    ```
    """
    response = client.post("/api/v1/transactions/", json=test_transaction)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["amount"] == test_transaction["amount"]
    assert data["type"] == test_transaction["type"]


def test_list_transactions_api(client):
    """Test retrieving all transactions.
    
    Equivalent curl command:
    ```bash
    curl -X GET http://localhost:8000/api/v1/transactions/
    
    # With filters:
    curl -X GET 'http://localhost:8000/api/v1/transactions/?status=pending&start_date=2024-03-01&end_date=2024-03-14'
    ```
    """
    response = client.get("/api/v1/transactions/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_transaction_api(client, test_transaction):
    """Test retrieving a specific transaction.
    
    Equivalent curl command:
    ```bash
    curl -X GET http://localhost:8000/api/v1/transactions/1
    ```
    """
    # First create a transaction
    create_response = client.post("/api/v1/transactions/", json=test_transaction)
    transaction_id = create_response.json()["id"]
    
    # Then retrieve it
    response = client.get(f"/api/v1/transactions/{transaction_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == transaction_id


def test_update_transaction_api(client, test_transaction):
    """Test updating a transaction.
    
    Equivalent curl command:
    ```bash
    curl -X PUT http://localhost:8000/api/v1/transactions/1 \
         -H "Content-Type: application/json" \
         -d '{
             "amount": 150.0,
             "currency": "USD",
             "type": "expense",
             "status": "posted",
             "category": "groceries",
             "description": "Updated transaction",
             "transaction_date": "2024-03-14T00:00:00Z",
             "posted_date": "2024-03-14T00:00:00Z",
             "plaid_item_id": 1,
             "plaid_account_id": 1
         }'
    ```
    """
    # First create a transaction
    create_response = client.post("/api/v1/transactions/", json=test_transaction)
    transaction_id = create_response.json()["id"]
    
    # Update the transaction
    update_data = dict(test_transaction)
    update_data["description"] = "Updated transaction"
    update_data["amount"] = 150.0
    
    response = client.put(f"/api/v1/transactions/{transaction_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["description"] == "Updated transaction"
    assert response.json()["amount"] == 150.0


def test_delete_transaction_api(client, test_transaction):
    """Test deleting a transaction.
    
    Equivalent curl command:
    ```bash
    curl -X DELETE http://localhost:8000/api/v1/transactions/1
    ```
    """
    # First create a transaction
    create_response = client.post("/api/v1/transactions/", json=test_transaction)
    transaction_id = create_response.json()["id"]
    
    # Delete the transaction
    response = client.delete(f"/api/v1/transactions/{transaction_id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/transactions/{transaction_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_filter_transactions_api(client, test_transaction):
    """Test filtering transactions by various parameters.
    
    Equivalent curl commands:
    ```bash
    # Filter by status
    curl -X GET 'http://localhost:8000/api/v1/transactions/?status=pending'
    
    # Filter by date range
    curl -X GET 'http://localhost:8000/api/v1/transactions/?start_date=2024-03-01&end_date=2024-03-14'
    
    # Filter by type
    curl -X GET 'http://localhost:8000/api/v1/transactions/?type=expense'
    
    # Filter by category
    curl -X GET 'http://localhost:8000/api/v1/transactions/?category=groceries'
    
    # Combined filters
    curl -X GET 'http://localhost:8000/api/v1/transactions/?status=pending&type=expense&category=groceries'
    ```
    """
    # Create a test transaction
    client.post("/api/v1/transactions/", json=test_transaction)
    
    # Test various filters
    filters = [
        "?status=pending",
        "?type=expense",
        f"?category={test_transaction['category']}",
        "?start_date=2024-03-01&end_date=2024-03-31"
    ]
    
    for filter_query in filters:
        response = client.get(f"/api/v1/transactions/{filter_query}")
        assert response.status_code == status.HTTP_200_OK 