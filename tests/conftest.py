"""
Test configuration and fixtures.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from plaid.model.item_public_token_exchange_response import ItemPublicTokenExchangeResponse
from plaid.model.transactions_get_response import TransactionsGetResponse
from plaid.model.account_base import AccountBase
from plaid.model.transaction import Transaction as PlaidTransaction
from plaid.model.link_token_create_response import LinkTokenCreateResponse

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.plaid import PlaidItem, PlaidAccount
from app.models.transaction import Transaction
from app.schemas.enums import TransactionTypeEnum, TransactionStatusEnum

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite://"

@pytest.fixture
def db():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    """Create a test client."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def mock_plaid_client():
    """Create a mock Plaid client."""
    mock_client = Mock()
    
    # Mock ItemPublicTokenExchangeResponse with required request_id
    mock_exchange_response = Mock(spec=ItemPublicTokenExchangeResponse)
    mock_exchange_response.access_token = "test_access_token"
    mock_exchange_response.item_id = "test_item_id"
    mock_exchange_response.request_id = "test_request_id"
    mock_client.item_public_token_exchange.return_value = mock_exchange_response
    
    # Mock TransactionsGetResponse with required fields
    mock_transactions_response = Mock(spec=TransactionsGetResponse)
    mock_transactions_response.accounts = []
    mock_transactions_response.transactions = []
    mock_transactions_response.request_id = "test_request_id"
    mock_transactions_response.total_transactions = 0
    mock_client.transactions_get.return_value = mock_transactions_response
    
    # Mock LinkTokenCreateResponse with required fields
    mock_link_token_response = Mock(spec=LinkTokenCreateResponse)
    mock_link_token_response.link_token = "test_link_token"
    mock_link_token_response.request_id = "test_request_id"
    mock_link_token_response.expiration = "2024-12-31"
    mock_client.link_token_create.return_value = mock_link_token_response
    
    return mock_client

@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password="test_password_hash"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_plaid_item(db, test_user):
    """Create a test Plaid item."""
    item = PlaidItem(
        item_id="test_item_id",
        access_token="test_access_token",
        institution_id="ins_123",
        institution_name="Test Bank"
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@pytest.fixture
def test_plaid_account(db, test_plaid_item):
    """Create a test Plaid account."""
    account = PlaidAccount(
        plaid_item_id=test_plaid_item.id,
        account_id="test_account_id",
        name="Test Account",
        type="depository",
        subtype="checking"
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

@pytest.fixture
def test_transaction(test_user, test_plaid_account):
    return {
        "amount": 100.0,
        "currency": "USD",
        "type": TransactionTypeEnum.EXPENSE.value,
        "status": TransactionStatusEnum.PENDING.value,
        "category": "groceries",
        "description": "Test transaction",
        "transaction_date": datetime.utcnow().isoformat(),
        "posted_date": datetime.utcnow().isoformat(),
        "plaid_item_id": test_plaid_account.plaid_item_id,
        "plaid_account_id": test_plaid_account.id,
        "user_id": test_user.id
    } 