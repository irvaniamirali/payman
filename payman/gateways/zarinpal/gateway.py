from ...http import API
from ...unified import AsyncSyncMixin
from ..interface import GatewayInterface

from .models import (
    CallbackParams,
    PaymentRequest,
    PaymentResponse
)
from .components.client import Client
from .components.base_url_builder import BaseURLBuilder
from .components.error_handler import ErrorHandler
from .methods import Methods


class ZarinPal(
    Methods,
    GatewayInterface[
        PaymentRequest,
        PaymentResponse,
        CallbackParams
    ],
    AsyncSyncMixin
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
            Version (int): API version. Default is 4.
            Sandbox (bool): Whether to use the sandbox environment. Default is False.
            client_options: Extra keyword arguments for the API HTTP client.
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
        return (f"<ZarinPal merchant_id={self.merchant_id!r} base_url={self.base_url!r} "
                f"sandbox={self.sandbox}>")
