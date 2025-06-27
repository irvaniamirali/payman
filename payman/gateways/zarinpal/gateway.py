from typing import Any

from ...http import API
from ...unified import AsyncCapable
from ...errors import PaymentGatewayManager
from ..interface import GatewayInterface

from .models import (
    CallbackParams,
    PaymentRequest,
    PaymentResponse,
    PaymentMetadata,
    ReverseRequest,
    ReverseResponse,
    UnverifiedPayments,
    VerifyRequest,
    VerifyResponse,
)


class ZarinPal(
    GatewayInterface[PaymentRequest, PaymentResponse, CallbackParams], AsyncCapable
):
    """
    ZarinPal payment gateway client.

    Implements all required operations for initiating, managing, and verifying
    payment transactions using the ZarinPal API. Compatible with both sync and async code.

    API Reference: https://docs.zarinpal.com/paymentGateway/
    """

    __BASE_DOMAIN = {
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
        self.base_url = self._build_base_url()
        self.client = API(base_url=self.base_url, **client_options)

    def __repr__(self):
        return f"<ZarinPal merchant_id={self.merchant_id!r} base_url={self.base_url!r}>"

    def _build_base_url(self) -> str:
        domain = self.__BASE_DOMAIN[self.sandbox]
        return f"https://{domain}/pg/v{self.version}/payment"

    async def _post(self, endpoint: str, payload: dict[str, Any] = None) -> dict[str, Any]:
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
        data = {"merchant_id": self.merchant_id, **payload}
        response = await self.client.request("POST", endpoint, json=data)

        if not response:
            raise RuntimeError("Empty response from ZarinPal API.")

        if errors := response.get("errors"):
            raise PaymentGatewayManager.handle_error(
                "ZarinPal",
                errors.get("code"),
                errors.get("message"),
            )

        return response

    def _format_metadata(self, metadata: PaymentMetadata | dict[str, Any] | None) -> list[dict[str, str]]:
        """
        Format metadata into ZarinPal-compliant key/value pairs.

        Args:
            metadata (PaymentMetadata | dict | None): Optional metadata.

        Returns:
            list[dict[str, str]]: Formatted metadata list.
        """
        if not metadata:
            return []

        if isinstance(metadata, dict):
            items = metadata.items()
        else:
            items = metadata.model_dump(exclude_none=True).items()

        return [{"key": str(k), "value": str(v)} for k, v in items]

    async def payment(self, request: PaymentRequest) -> PaymentResponse:
        """
        Create a payment session and retrieve an authority code.

        Args:
            request (PaymentRequest): The payment request details.

        Returns:
            PaymentResponse: The response containing the authority and status.
        """
        payload = request.model_dump(mode="json")
        payload["metadata"] = self._format_metadata(payload.get("metadata"))
        response = await self._post("/request.json", payload)
        return PaymentResponse(**response.get("data"))

    def get_payment_redirect_url(self, authority: str) -> str:
        """
        Construct the full URL to redirect the user to the payment gateway page.

        Args:
            authority (str): The unique authority or token received from a successful payment initiation.

        Returns:
            str: A complete URL where the customer should be redirected to complete the payment process.
        """
        domain = self.__BASE_DOMAIN[self.sandbox]
        return f"https://{domain}/pg/StartPay/{authority}"

    async def verify(self, request: VerifyRequest) -> VerifyResponse:
        """
        Verify the transaction status after the payment is complete.

        Args:
            request (VerifyRequest): The verification request.

        Returns:
            VerifyResponse: Verification result including ref_id.
        """
        payload = request.model_dump(mode="json")
        response = await self._post("/verify.json", payload)
        return VerifyResponse(**response.get("data"))

    async def reverse(self, request: ReverseRequest) -> ReverseResponse:
        """
        Reverse a pending or unsettled transaction.

        Args:
            request (ReverseRequest): Details of the transaction to reverse.

        Returns:
            ReverseResponse: Result of the reversal process.
        """
        payload = request.model_dump(mode="json")
        response = await self._post("/reverse.json", payload)
        return ReverseResponse(**response.get("data"))

    async def get_unverified_payments(self) -> UnverifiedPayments:
        """
        Fetch the list of successful but not-yet-verified payments from ZarinPal.

        Returns:
            UnverifiedResponse: Contains status code, message, and a list of unverified transactions.
        """
        response = await self._post("/unVerified.json")
        return UnverifiedPayments(**response.get("data"))
