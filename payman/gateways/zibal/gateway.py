from typing import Any, ClassVar

from ...http import API
from ...unified import AsyncCapable
from ...errors import PaymentGatewayManager
from ..interface import GatewayInterface
from .models import (
    CallbackParams,
    InquiryRequest,
    InquiryResponse,
    PaymentRequest,
    PaymentResponse,
    VerifyRequest,
    VerifyResponse,
)


class Zibal(GatewayInterface[PaymentRequest, PaymentResponse, CallbackParams], AsyncCapable):
    """
    Zibal payment gateway client implementing required operations
    for initiating, verifying, inquiring, and refunding payment transactions.

    API Reference: https://help.zibal.ir/IPG/API/
    """

    BASE_URL: ClassVar[str] = "https://gateway.zibal.ir"

    def __init__(
            self,
            merchant_id: str,
            version: int = 1,
            **client_options
    ):
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
        self.client = API(base_url=self.base_url, **client_options)

    def __repr__(self):
        return f"<Zibal merchant_id={self.merchant_id!r} base_url={self.base_url!r}>"

    async def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = {"merchant": self.merchant_id, **payload}
        response = await self.client.request("POST", endpoint, json=data)
        if response.get("result") != 100:
            raise PaymentGatewayManager.handle_error(
                "Zibal", response.get("result"), response.get("message")
            )
        return response

    async def payment(self, request: PaymentRequest) -> PaymentResponse:
        """
        Initiate a new payment request.

        Args:
            request (PaymentRequest): Payment input parameters.

        Returns:
            PaymentResponse: Contains result code and track ID.
        """
        payload = request.model_dump(by_alias=True, mode="json")
        response = await self._post("/request", payload)
        return PaymentResponse(**response)

    def get_payment_redirect_url(self, track_id: int) -> str:
        """
        Generate a user payment URL for redirecting to Zibal gateway.

        Args:
        track_id (int): Track ID received from `payment()` or `lazy_payment()`.

        Returns:
        str: Full redirect URL to Zibal payment page.
        """
        return f"{self.BASE_URL}/start/{track_id}"

    async def verify(self, request: VerifyRequest) -> VerifyResponse:
        """
        Verify the payment after redirect or callback.

        Args:
            request (VerifyRequest): Track ID to verify.

        Returns:
            VerifyResponse: Verification result with transaction details.
        """
        payload = request.model_dump(by_alias=True, mode="json")
        response = await self._post("/verify", payload)
        return VerifyResponse(**response)

    async def callback_verify(self, callback: CallbackParams) -> VerifyResponse:
        """
        Verify server-to-server callback from Zibal (lazy verification).

        Args:
            callback (CallbackParams): Payload received in Zibal's callback request.

        Returns:
            VerifyResponse: Transaction info and status.
        """
        payload = callback.model_dump(by_alias=True, mode="json")
        response = await self._post("/callback/verify", payload)
        return VerifyResponse(**response)

    async def inquiry(self, request: InquiryRequest) -> InquiryResponse:
        """
        Inquire the current state of a payment.

        Args:
            request (InquiryRequest): Track ID or order ID.

        Returns:
            InquiryResponse: Current status and transaction details.
        """
        payload = request.model_dump(by_alias=True, mode="json")
        response = await self._post("/inquiry", payload)
        return InquiryResponse(**response)

    async def lazy_payment(self, request: PaymentRequest) -> PaymentResponse:
        """
        Initiate a lazy (delayed verification) payment.

        Args:
            request (PaymentRequest): Payment input parameters.

        Returns:
            PaymentResponse: Result of payment initiation.
        """
        payload = request.model_dump(by_alias=True, mode="json")
        response = await self._post("/request/lazy", payload)
        return PaymentResponse(**response)
