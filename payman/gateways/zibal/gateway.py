from typing import ClassVar

from ...http import API
from ...unified import AsyncSyncMixin
from ..interface import GatewayInterface
from .models import (
    CallbackParams,
    PaymentRequest,
    PaymentResponse,
)
from .components.client import Client
from .components.error_handler import ErrorHandler
from .methods import Methods


class Zibal(
    Methods,
    GatewayInterface[
        PaymentRequest,
        PaymentResponse,
        CallbackParams
    ],
    AsyncSyncMixin
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
            Version (int): API version (default is 1).
            client_options: Additional parameters for the HTTP client.
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
