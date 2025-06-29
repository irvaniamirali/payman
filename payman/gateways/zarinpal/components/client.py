from typing import Any
from payman.http import API
from .error_handler import ErrorHandler


class APIClient:
    def __init__(
            self, merchant_id: str, base_url: str, client: API, error_handler: ErrorHandler
    ):
        self.merchant_id = merchant_id
        self.base_url = base_url
        self.client = client
        self.error_handler = error_handler

    async def post(self, endpoint: str, payload: dict[str, Any] = None) -> dict[str, Any]:
        """
        Send a POST request to the ZarinPal API with standardized error handling.

        Args:
            endpoint (str): API endpoint (e.g., '/request.json').
            payload (dict): Data to send in the request.

        Returns:
            dict: Parsed JSON response.

        Raises:
            PaymentGatewayError: If the response contains errors.
        """
        data = {"merchant_id": self.merchant_id, **(payload or {})}
        response = await self.client.request("POST", endpoint, json=data)
        self.error_handler.handle(response)
        return response
