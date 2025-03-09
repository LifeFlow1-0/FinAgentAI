"""
Test configuration and fixtures.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from plaid.model.item_public_token_exchange_response import ItemPublicTokenExchangeResponse
from plaid.model.transactions_get_response import TransactionsGetResponse

from app.database import Base, get_db
from app.main import app

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    # Create tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db):
    """Test client with database dependency override."""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def mock_plaid_client():
    """Mock Plaid client for testing."""
    with patch("app.utils.plaid_client.get_plaid_client") as mock:
        client = Mock()
        
        # Mock link token creation
        client.link_token_create.return_value.link_token = "test_link_token"
        
        # Mock public token exchange
        exchange_response = Mock(spec=ItemPublicTokenExchangeResponse)
        exchange_response.access_token = "test_access_token"
        exchange_response.item_id = "test_item_id"
        client.item_public_token_exchange.return_value = exchange_response
        
        # Mock transactions
        transactions_response = Mock(spec=TransactionsGetResponse)
        transactions_response.accounts = []
        transactions_response.transactions = []
        client.transactions_get.return_value = transactions_response
        
        mock.return_value = client
        yield client 