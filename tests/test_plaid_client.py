"""
Tests for Plaid client integration.
"""
import pytest
from app.utils.plaid_client import get_plaid_client, create_link_token, PlaidError

def test_plaid_client_initialization():
    """Test that we can initialize the Plaid client with our credentials."""
    try:
        client = get_plaid_client()
        assert client is not None, "Plaid client should be initialized"
    except PlaidError as e:
        pytest.fail(f"Failed to initialize Plaid client: {str(e)}")

def test_create_link_token_without_redirect():
    """Test that we can create a link token without OAuth redirect."""
    try:
        client = get_plaid_client()
        link_token = create_link_token(client, "test_user_id", use_redirect=False)
        assert link_token is not None, "Link token should be created"
        assert isinstance(link_token, str), "Link token should be a string"
    except PlaidError as e:
        pytest.fail(f"Failed to create link token without redirect: {str(e)}")

def test_create_link_token_with_redirect():
    """Test that we can create a link token with OAuth redirect."""
    try:
        client = get_plaid_client()
        link_token = create_link_token(client, "test_user_id", use_redirect=True)
        assert link_token is not None, "Link token should be created"
        assert isinstance(link_token, str), "Link token should be a string"
    except PlaidError as e:
        pytest.fail(f"Failed to create link token with redirect: {str(e)}") 