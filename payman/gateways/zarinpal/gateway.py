from payman.http import API
from payman.unified import AsyncSyncMixin
from payman.gateways.interface import GatewayInterface

from .models import CallbackParams, PaymentRequest, PaymentResponse
from .components.client import Client
from .components.base_url_builder import BaseURLBuilder
from .components.error_handler import ErrorHandler
from .methods import Methods


class ZarinPal(
    # High-level interface (business logic interface)
    Methods,
    # Core behavior and contract
    GatewayInterface[PaymentRequest, PaymentResponse, CallbackParams],
    # Runtime utility behavior (sync/async support)
    AsyncSyncMixin,
):
    """
    ZarinPal payment gateway client.

    Implements all required operations for initiating, managing, and verifying
    payment transactions using the ZarinPal API. Compatible with both sync and async code.

    API Reference: https://docs.zarinpal.com/paymentGateway/
    """

    _BASE_DOMAIN = {
        True: "sandbox.zarinpal.com",
        False: "www.zarinpal.com"
    }

    def __init__(
        self,
        merchant_id: str,
        version: int = 4,
        sandbox: bool = False,
        **client_options,
    ):
        """
        Initialize a ZarinPal client.

        Args:
            merchant_id (str): The merchant ID (UUID) provided by ZarinPal.
            version (int): API version. Default is 4.
            sandbox (bool): Whether to use the sandbox environment. Default is False.
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
        if not merchant_id or not isinstance(merchant_id, str):
            raise ValueError("`merchant_id` must be a non-empty string.")

        self.merchant_id = merchant_id
        self.version = version
        self.sandbox = sandbox
        self.base_url = BaseURLBuilder(self.sandbox, self.version)
        self.error_handler = ErrorHandler()
        self.client = Client(
            merchant_id=self.merchant_id,
            base_url=self.base_url,
            client=API(base_url=self.base_url, **client_options),
            error_handler=self.error_handler,
        )

    def __repr__(self):
        return (
            f"<ZarinPal merchant_id={self.merchant_id!r} base_url={self.base_url!r} "
            f"sandbox={self.sandbox}>"
        )
