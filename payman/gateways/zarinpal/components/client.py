from typing import Any
from payman.http import API
from .error_handler import ErrorHandler


class Client:
    """
    A client wrapper to send POST requests with merchant identification
    and centralized error handling.
    """

    def __init__(
            self,
            merchant_id: str,
            base_url: str,
            client: API,
            error_handler: ErrorHandler,
    ) -> None:
        """
        Initialize API Client.

        Args:
            merchant_id (str): Merchant identifier for requests.
            base_url (str): Base URL of the API.
            client (API): HTTP client instance to perform requests.
            error_handler (ErrorHandler): Error handler for API responses.
        """
        self.merchant_id = merchant_id
        self.base_url = base_url
        self.client = client
        self.error_handler = error_handler

    async def post(self, endpoint: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Send a POST request to the payment gateway API with standardized error handling.

        Args:
            endpoint (str): API endpoint (e.g., '/request.json').
            payload (dict[str, Any] | None = None): Data to include in the request body.

        Returns:
            dict[str, Any]: Parsed JSON response.

        Raises:
            PaymentGatewayError: If the API response contains an error.
        """
        response = await self.client.request(
            "POST", endpoint, json={"merchant_id": self.merchant_id, **(payload or {})}
        )
        self.error_handler.handle(response)
        return response
