from typing import Any, Dict
from ...http import API
from ...unified import Asyncifiable
from ...interface import BaseGateway
from .models import (
    CallbackParams,
    PaymentRequest,
    PaymentResponse,
    PaymentMetadata,
    PaymentVerifyRequest,
    PaymentVerifyResponse,
)
from .errors import ZarinPalVerificationError, ZARINPAL_ERROR_MESSAGES


class ZarinPal(BaseGateway, Asyncifiable):
    """
    ZarinPal Payment Gateway Client.
    """
    def __init__(self, merchant_id: str, version: int = 4, sandbox: bool = False, **client_params):
        """
        :param merchant_id: Merchant UUID provided by ZarinPal
        :param version: API version (default v4)
        :param sandbox: Whether to use sandbox domain (default: False)
        :param client_params: Optional parameters for the HTTP client
        """
        self.merchant_id = merchant_id
        self.version = version
        self.sandbox = sandbox
        self.base_url = self._build_base_url()
        self.client = API(base_url=self.base_url, **client_params)

    def _build_base_url(self) -> str:
        """
        Constructs the base URL depending on sandbox usage.
        """
        domain = "sandbox.zarinpal.com" if self.sandbox else "payment.zarinpal.com"
        return f"https://{domain}/pg/v{self.version}/payment"

    async def request(self, method: str, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """        self.version = version

        Sends an HTTP request with the merchant ID included.

        :param method: HTTP method ('POST', etc.)
        :param endpoint: API endpoint
        :param payload: Dictionary payload to send in JSON body
        :return: Parsed response as a dict
        """
        data = {"merchant_id": self.merchant_id, **payload}
        return await self.client.request(method, endpoint, json=data)

    @staticmethod
    def _prepare_metadata(metadata: PaymentMetadata | Dict[str, Any] | None) -> list[Dict[str, str]]:
        """
        Converts metadata into ZarinPal expected format.

        :param metadata: dict, PaymentMetadata instance, or None
        :return: List of {"key": str, "value": str} items
        """
        if metadata is None:
            return []

        if isinstance(metadata, dict):
            return [{"key": k, "value": str(v)} for k, v in metadata.items()]

        # Assume metadata is a Pydantic model
        model_dict = metadata.model_dump(exclude_none=True)
        return [{"key": k, "value": str(v)} for k, v in model_dict.items()]

    async def request_payment(self, req: PaymentRequest) -> PaymentResponse:
        """
        Creates a new payment session.

        :param req: PaymentRequest model with amount, callback URL, etc.
        :return: PaymentResponse including authority code
        """
        data = req.model_dump(mode="json")
        data["metadata"] = self._prepare_metadata(data.get("metadata"))

        resp = await self.request("POST", "/request.json", data)
        return PaymentResponse(**resp)

    async def verify(self, req: PaymentVerifyRequest) -> PaymentVerifyResponse:
        """
        Verifies a completed transaction using authority and amount.

        :param req: PaymentVerifyRequest including authority and amount
        :return: PaymentVerifyResponse model
        :raises: ZarinPalVerificationError on failure or unknown code
        """
        payload = {"authority": req.authority, "amount": req.amount}
        resp = await self.request("POST", "/verify.json", payload)

        data = resp.get("data")
        if not isinstance(data, dict):
            raise ZarinPalVerificationError(-99, "Invalid response structure from ZarinPal.")

        verify_response = PaymentVerifyResponse(**data)

        if verify_response.code not in (100, 101):
            msg = ZARINPAL_ERROR_MESSAGES.get(verify_response.code, verify_response.message or "Unknown verification error")
            raise ZarinPalVerificationError(verify_response.code, msg)

        return verify_response

    def payment_url_generator(self, authority: str) -> str:
        """
        Generates the final URL for redirecting user to payment gateway.

        :param authority: Authority code returned by `request_payment`
        :return: Full redirect URL
        """
        domain = "sandbox.zarinpal.com" if self.sandbox else "payment.zarinpal.com"
        return f"https://{domain}/pg/StartPay/{authority}"
