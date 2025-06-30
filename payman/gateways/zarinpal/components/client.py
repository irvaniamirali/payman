from typing import Any, Dict, Optional
from payman.http import API
from .error_handler import ErrorHandler


class Client:
    def __init__(
            self,
            merchant_id: str,
            base_url: str,
            client: API,
            error_handler: ErrorHandler,
    ) -> None:
        self.merchant_id = merchant_id
        self.base_url = base_url
        self.client = client
        self.error_handler = error_handler

    async def post(self, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a POST request to the payment gateway API with standardized error handling.

        Args:
            endpoint (str): API endpoint (e.g., '/request.json').
            payload (Optional[Dict[str, Any]]): Data to include in the request body.

        Returns:
            Dict[str, Any]: Parsed JSON response.

        Raises:
            PaymentGatewayError: If the API response contains an error.
        """
        data = {"merchant_id": self.merchant_id, **(payload or {})}
        response = await self.client.request("POST", endpoint, json=data)
        self.error_handler.handle(response)
        return response
