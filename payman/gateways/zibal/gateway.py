from typing import ClassVar

from payman.http import API
from payman.unified import AsyncSyncMixin
from payman.gateways.interface import GatewayInterface

from .models import (
    CallbackParams,
    PaymentRequest,
    PaymentResponse,
)
from .components.client import Client
from .components.error_handler import ErrorHandler
from .methods import Methods


class Zibal(
    # High-level interface (business logic interface)
    Methods,
    # Core behavior and contract
    GatewayInterface[PaymentRequest, PaymentResponse, CallbackParams],
    # Runtime utility behavior (sync/async support)
    AsyncSyncMixin,
):
    """
    Zibal payment gateway client implementing required operations
    for initiating, verifying, inquiring, and refunding payment transactions.

    API Reference: https://help.zibal.ir/IPG/API/
    """

    BASE_URL: ClassVar[str] = "https://gateway.zibal.ir"

    def __init__(self, merchant_id: str, version: int = 1, **client_options):
        """
        Initialize the Zibal client.

        Args:
            merchant_id (str): Your merchant ID provided by Zibal.
            version (int): API version (default is 1).
            client_options: Additional options passed to the internal HTTP client.
                Supported options include:
                    - timeout (int): Request timeout in seconds. Default is 10.
                    - max_retries (int): Number of retry attempts. Default is 0.
                    - retry_delay (float): Delay between retries in seconds. Default is 1.0.
                    - slow_request_threshold (float): Log if request exceeds this threshold. Default is 3.0.
                    - log_level (int): Logging level (e.g., logging.INFO). Default is INFO.
                    - log_request_body (bool): Log request body (for debugging). Default is True.
                    - log_response_body (bool): Log response body. Default is True.
                    - max_log_body_length (int): Max size of request/response to log. Default is 500.
                    - default_headers (dict): Extra headers to send with each request.

        Raises:
            ValueError: If `merchant_id` is empty or invalid.
        """
        if not isinstance(merchant_id, str) or not merchant_id:
            raise ValueError("`merchant_id` must be a non-empty string")

        self.merchant_id = merchant_id
        self.base_url = f"{self.BASE_URL}/v{version}"
        self.error_handler = ErrorHandler()
        self.client = Client(
            merchant_id=self.merchant_id,
            base_url=self.base_url,
            client=API(base_url=self.base_url, **client_options),
            error_handler=self.error_handler,
        )

    def __repr__(self):
        return f"<Zibal merchant_id={self.merchant_id!r} base_url={self.base_url!r}>"
