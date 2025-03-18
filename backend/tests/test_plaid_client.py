"""
Tests for Plaid client integration.
"""
from unittest.mock import Mock, patch

import pytest
from plaid.model.link_token_create_response import LinkTokenCreateResponse

from app.utils.plaid_client import PlaidError, create_link_token, get_plaid_client


@patch("app.utils.plaid_client.Configuration")
@patch("app.utils.plaid_client.ApiClient")
@patch("app.utils.plaid_client.plaid_api.PlaidApi")
def test_plaid_client_initialization(mock_plaid_api, mock_api_client, mock_config):
    """Test that we can initialize the Plaid client with our credentials."""
    try:
        mock_plaid_api.return_value = Mock()
        client = get_plaid_client()
        assert client is not None, "Plaid client should be initialized"
        mock_config.assert_called_once()
        mock_api_client.assert_called_once()
        mock_plaid_api.assert_called_once()
    except PlaidError as e:
        pytest.fail(f"Failed to initialize Plaid client: {str(e)}")


@patch("app.utils.plaid_client.Configuration")
@patch("app.utils.plaid_client.ApiClient")
@patch("app.utils.plaid_client.plaid_api.PlaidApi")
def test_create_link_token_without_redirect(mock_plaid_api, mock_api_client, mock_config):
    """Test that we can create a link token without OAuth redirect."""
    try:
        # Setup mock response
        mock_response = Mock(spec=LinkTokenCreateResponse)
        mock_response.link_token = "test_link_token"
        mock_client = Mock()
        mock_client.link_token_create.return_value = mock_response
        mock_plaid_api.return_value = mock_client

        client = get_plaid_client()
        link_token = create_link_token(client, "test_user_id", use_redirect=False)
        
        assert link_token is not None, "Link token should be created"
        assert isinstance(link_token, str), "Link token should be a string"
        assert link_token == "test_link_token", "Link token should match mock response"
        mock_client.link_token_create.assert_called_once()
    except PlaidError as e:
        pytest.fail(f"Failed to create link token without redirect: {str(e)}")


@patch("app.utils.plaid_client.Configuration")
@patch("app.utils.plaid_client.ApiClient")
@patch("app.utils.plaid_client.plaid_api.PlaidApi")
def test_create_link_token_with_redirect(mock_plaid_api, mock_api_client, mock_config):
    """Test that we can create a link token with OAuth redirect."""
    try:
        # Setup mock response
        mock_response = Mock(spec=LinkTokenCreateResponse)
        mock_response.link_token = "test_link_token_with_redirect"
        mock_client = Mock()
        mock_client.link_token_create.return_value = mock_response
        mock_plaid_api.return_value = mock_client

        client = get_plaid_client()
        link_token = create_link_token(client, "test_user_id", use_redirect=True)
        
        assert link_token is not None, "Link token should be created"
        assert isinstance(link_token, str), "Link token should be a string"
        assert link_token == "test_link_token_with_redirect", "Link token should match mock response"
        mock_client.link_token_create.assert_called_once()
    except PlaidError as e:
        pytest.fail(f"Failed to create link token with redirect: {str(e)}") 