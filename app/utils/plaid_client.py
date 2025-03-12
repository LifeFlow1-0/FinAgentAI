"""
Plaid API client utility.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from plaid.api import plaid_api
from plaid.api_client import ApiClient
from plaid.configuration import Configuration
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

from app.config import settings


class PlaidError(Exception):
    """Custom exception for Plaid API errors."""

    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


def get_plaid_client() -> plaid_api.PlaidApi:
    """
    Initialize and return a Plaid API client.

    Raises:
        PlaidError: If client initialization fails
    """
    try:
        configuration = Configuration(
            host=f"https://{settings.PLAID_ENV}.plaid.com",
            api_key={
                "clientId": settings.PLAID_CLIENT_ID,
                "secret": settings.PLAID_SECRET,
            },
        )
        api_client = ApiClient(configuration)
        client = plaid_api.PlaidApi(api_client)
        return client
    except Exception as e:
        raise PlaidError(f"Failed to initialize Plaid client: {str(e)}")


def create_link_token(
    client: plaid_api.PlaidApi, user_id: str, use_redirect: bool = False
) -> str:
    """
    Create a Link token for initializing Plaid Link.

    Args:
        client: Plaid API client
        user_id: Unique identifier for the user
        use_redirect: Whether to use OAuth redirect

    Returns:
        str: Link token

    Raises:
        PlaidError: If token creation fails
    """
    try:
        request_args = {
            "products": [Products("transactions")],
            "client_name": "LifeFlow",
            "country_codes": [CountryCode("US")],
            "language": "en",
            "user": LinkTokenCreateRequestUser(client_user_id=user_id),
        }

        if use_redirect:
            request_args["redirect_uri"] = settings.PLAID_REDIRECT_URI

        request = LinkTokenCreateRequest(**request_args)
        response = client.link_token_create(request)
        return response.link_token
    except Exception as e:
        raise PlaidError(f"Failed to create link token: {str(e)}")


def exchange_public_token(
    client: plaid_api.PlaidApi, public_token: str
) -> tuple[str, str]:
    """
    Exchange a public token for an access token.

    Args:
        client: Plaid API client
        public_token: Public token from Plaid Link

    Returns:
        tuple: (access_token, item_id)

    Raises:
        PlaidError: If token exchange fails
    """
    try:
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = client.item_public_token_exchange(request)
        return response.access_token, response.item_id
    except Exception as e:
        raise PlaidError(f"Failed to exchange public token: {str(e)}")


def get_transactions(
    client: plaid_api.PlaidApi,
    access_token: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> dict:
    """
    Retrieve transactions for a connected account.

    Args:
        client: Plaid API client
        access_token: Plaid access token for the account
        start_date: Start date for transactions (defaults to 30 days ago)
        end_date: End date for transactions (defaults to today)

    Returns:
        dict: Transaction data

    Raises:
        PlaidError: If transaction retrieval fails
    """
    try:
        start_date = start_date or (datetime.now() - timedelta(days=30))
        end_date = end_date or datetime.now()

        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date.date(),
            end_date=end_date.date(),
            options=TransactionsGetRequestOptions(
                include_personal_finance_category=True
            ),
        )
        response = client.transactions_get(request)
        return {"accounts": response.accounts, "transactions": response.transactions}
    except Exception as e:
        raise PlaidError(f"Failed to retrieve transactions: {str(e)}")


def handle_plaid_error(error: Exception) -> HTTPException:
    """Convert Plaid errors to FastAPI HTTP exceptions."""
    if isinstance(error, PlaidError):
        return HTTPException(
            status_code=400,
            detail={"message": error.message, "error_code": error.error_code},
        )
    return HTTPException(
        status_code=500,
        detail={"message": "Internal server error", "error": str(error)},
    )
