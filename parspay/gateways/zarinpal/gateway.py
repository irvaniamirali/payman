from typing import Optional, Dict, Union, Any, List
from parspay.http import API
from .models import (
    Payment,
    PaymentVerify,
    VerifyPaymentResponse,
    PaymentResponse,
    PaymentMetadata,
    CallbackParams,
)
from .errors import ZarinPalVerificationError


class ZarinPal:
    """
    ZarinPal Payment Gateway Client

    Handles creating payments, generating payment URLs,
    processing callback parameters, and verifying payments.
    """

    VERIFY_ENDPOINT = "/verify.json"
    REQUEST_ENDPOINT = "/request.json"
    START_PAY_PATH = "/StartPay"

    def __init__(
            self,
            merchant_id: str,
            version: int = 4,
            sandbox: bool = False,
            **client_params
    ):
        """
        Initialize the ZarinPal client.

        :param merchant_id: Unique merchant ID (UUID) provided by ZarinPal
        :param version: API version (default: 4)
        :param sandbox: Use sandbox environment for testing (default: False)
        :param client_params: Additional parameters for the HTTP client
        """
        self.merchant_id = merchant_id
        self.version = version
        self.sandbox = sandbox
        self.base_url = self._build_base_url()
        self.client = API(base_url=self.base_url, **client_params)

    def _build_base_url(self) -> str:
        """
        Build the base API URL based on sandbox flag and version.
        """
        domain = "sandbox.zarinpal.com" if self.sandbox else "payment.zarinpal.com"
        return f"https://{domain}/pg/v{self.version}/payment"

    async def request(self, method: str, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send an HTTP request to ZarinPal API with merchant_id added to payload.

        :param method: HTTP method (POST, GET, etc.)
        :param endpoint: API endpoint path
        :param params: Parameters to send in the request JSON body
        :return: Parsed JSON response as dict
        """
        payload = {'merchant_id': self.merchant_id, **params}
        return await self.client.request(method, endpoint, json=payload)

    @staticmethod
    def _prepare_metadata(metadata: Optional[Union[PaymentMetadata, Dict[str, Any]]]) -> List[Dict[str, str]]:
        """
        Normalize metadata into the expected list of key-value dicts.

        :param metadata: Either a dict, PaymentMetadata, or None
        :return: List of {"key": str, "value": str} dicts
        """
        if metadata is None:
            return []

        if isinstance(metadata, dict):
            return [{"key": k, "value": str(v)} for k, v in metadata.items()]

        # Assume PaymentMetadata model with dict() method
        data = metadata.model_dump(exclude_none=True)
        return [{"key": k, "value": str(v)} for k, v in data.items()]

    async def create_payment(self, payment: Payment) -> PaymentResponse:
        """
        Create a new payment request at ZarinPal.

        :param payment: Payment data model
        :return: PaymentResponse parsed from API response
        """
        payload = payment.model_dump(mode='json')
        payload['metadata'] = self._prepare_metadata(payload.get('metadata'))

        response = await self.request('POST', self.REQUEST_ENDPOINT, payload)
        return PaymentResponse(**response)

    def generate_payment_url(self, authority: str) -> str:
        """
        Generate URL to redirect user to ZarinPal payment page.

        :param authority: Authority code from create_payment response
        :return: Full URL string for redirection
        """
        base = self.base_url.rsplit('/payment', 1)[0]
        return f"{base}{self.START_PAY_PATH}/{authority}/ZarinGate"

    async def process_payment_callback(self, params: CallbackParams) -> None:
        """
        Handle callback from ZarinPal gateway.

        This method **does not verify** the payment; it only checks the status.
        The actual verify_payment call with the correct amount should be performed
        by the caller after this check.

        :param params: Callback parameters containing 'authority' and 'status'
        :raises ZarinPalVerificationError: If transaction was canceled or failed
        """
        if params.status != "OK":
            # Transaction failed or was cancelled by user
            raise ZarinPalVerificationError(-1, "Transaction cancelled or unsuccessful")

        # If status is OK, payment can be verified by caller
        # No return value here to enforce explicit verify call

    async def verify_payment(self, params: PaymentVerify) -> VerifyPaymentResponse:
        """
         Verify a payment transaction with ZarinPal by authority code and amount.

        :param params(PaymentVerify): Verification parameters including 'authority' and 'amount'
        :return VerifyPaymentResponse: Detailed verification response including status code, reference ID, fees, etc.
        :raises ZarinPalVerificationError: If verification fails or returns unexpected status code.
        """
        payload = {"authority": params.authority, "amount": params.amount}
        response = await self.request('POST', self.VERIFY_ENDPOINT, payload)

        verify_resp = VerifyPaymentResponse(
            code=response.get("code", 0),
            ref_id=response.get("ref_id"),
            card_pan=response.get("card_pan"),
            card_hash=response.get("card_hash"),
            fee_type=response.get("fee_type"),
            fee=response.get("fee"),
            message=response.get("message", ""),
        )

        # Accept only 100 (first success) or 101 (already verified success)
        if verify_resp.code not in (100, 101):
            raise ZarinPalVerificationError(verify_resp.code, verify_resp.message or "Unknown verification error")

        return verify_resp
