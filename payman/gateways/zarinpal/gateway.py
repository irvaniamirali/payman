from typing import Any, Dict
from payman.http import API
from payman.unified import Asyncifiable
from payman.errors.manager import PaymentGatewayManager
from payman.gateways.interface import GatewayInterface
from .models import (
    PaymentRequest,
    PaymentResponse,
    PaymentMetadata,
    PaymentVerifyRequest,
    PaymentVerifyResponse,
)


class ZarinPal(GatewayInterface, Asyncifiable):
    """
    ZarinPal Payment Gateway Client.
    """
    def __init__(self, merchant_id: str, version: int = 4, sandbox: bool = False, **client_params):
        """
        Initializes the ZarinPal Payment Gateway Client.

        :param merchant_id: Merchant UUID provided by ZarinPal.
        :param version: API version (default v4)
        :param sandbox: Whether to use sandbox domain (default: False)
        :param client_params: Additional parameters for the API client.
        """
        self.merchant_id = merchant_id
        self.version = version
        self.sandbox = sandbox
        self.base_url = self._build_base_url()
        self.client = API(base_url=self.base_url, **client_params)

    def _build_base_url(self) -> str:
        """
        Builds the base URL for the ZarinPal API based on the sandbox setting.

        :return: The base URL as a string.
        """
        domain = "sandbox.zarinpal.com" if self.sandbox else "payment.zarinpal.com"
        return f"https://{domain}/pg/v{self.version}/payment"

    async def request(self, method: str, endpoint: str, payload: Dict[str, Any]) -> dict[str, Any]:
        """
        Sends an HTTP request with the merchant ID included.

        :param method: HTTP method ('POST', etc.)
        :param endpoint: API endpoint
        :param payload: Dictionary payload to send in JSON body
        :return: Parsed response as a dict
        """
        data = {"merchant_id": self.merchant_id, **payload}
        response = await self.client.request(method, endpoint, json=data)
        if response.get("errors"):
            error_code = response["errors"].get("code")
            error_message = response["errors"].get("message")
            raise PaymentGatewayManager.handle_error("ZarinPal", error_code, error_message)
        return response

    @staticmethod
    def _prepare_metadata(metadata: PaymentMetadata | Dict[str, Any] | None) -> list[Dict[str, str]]:
        """
        Converts metadata into the format expected by ZarinPal.

        :param metadata: PaymentMetadata instance, dictionary, or None.
        :return: List of dictionaries with "key" and "value" pairs.
        """
        if metadata is None:
            return []

        if isinstance(metadata, dict):
            return [{"key": k, "value": str(v)} for k, v in metadata.items()]

        # Assume metadata is a Pydantic model
        model_dict = metadata.model_dump(exclude_none=True)
        return [{"key": k, "value": str(v)} for k, v in model_dict.items()]

    async def payment(self, request: PaymentRequest) -> PaymentResponse:
        """
        Creates a new payment session.

        This method sends a payment request to the ZarinPal API and returns the response
        containing the authority code and other payment details.

        :param request: An instance of PaymentRequest model with amount, callback URL, etc.
        :return: An instance of PaymentResponse including authority code.
        """
        data = request.model_dump(mode="json")
        data["metadata"] = self._prepare_metadata(data.get("metadata"))

        response = await self.request("POST", "/request.json", data)
        return PaymentResponse(**response)

    async def verify(self, request: PaymentVerifyRequest) -> PaymentVerifyResponse:
        """
        Verifies a completed transaction using authority and amount.

        This method checks the transaction status with the ZarinPal API and returns
        the verification result.

        :param request: An instance of PaymentVerifyRequest including authority and amount.
        :return: An instance of PaymentVerifyResponse model containing verification details.
        """
        response = await self.request("POST", "/verify.json", request.model_dump())
        data = response.get("data")
        return PaymentVerifyResponse(**data)

    def payment_url_generator(self, authority: str) -> str:
        """
        Generates the final URL for redirecting the user to the payment gateway.

        This method constructs the URL that the user will be redirected to for completing
        the payment process.

        :param authority: Authority code returned by the ZarinPal
        """
        domain = "sandbox.zarinpal.com" if self.sandbox else "payment.zarinpal.com"
        return f"https://{domain}/pg/StartPay/{authority}"
