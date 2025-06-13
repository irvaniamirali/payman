from typing import Dict, Any
from payman.http import API
from .models import (
    CallbackParams,
    LazyCallback,
    PaymentInquiryRequest,
    PaymentInquiryResponse,
    PaymentRequest,
    PaymentResponse,
    PaymentVerifyRequest,
    PaymentVerifyResponse,
)

from .interface import GatewayInterface

class Zibal(GatewayInterface):
    def __init__(
            self,
            merchant: str,
            version: int = 1,
            **client_params
    ):
        self.merchant = merchant
        self.version = version
        self.base_url = f"https://gateway.zibal.ir/v{self.version}/"
        self.client = API(base_url=self.base_url, **client_params)

    async def request(self, method: str, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send an HTTP request to the Zibal API.

        Args:
            method (str): HTTP method (e.g., 'POST').
            endpoint (str): Endpoint path (e.g., '/verify.json').
            params (Dict[str, Any]): JSON payload to send.

        Returns:
            Dict[str, Any]: Parsed JSON response.
        """
        payload = {'merchant': self.merchant, **params}
        return await self.client.request(method, endpoint, json=payload)

    async def request_payment(self, payment: PaymentRequest) -> PaymentResponse:
        resp = await self.request('POST', '/request', payment.model_dump(by_alias=True))
        return PaymentResponse(**resp)

    async def verify(self, verify_request: PaymentVerifyRequest) -> PaymentVerifyResponse:
        """
        Verifies the payment using the trackId returned in the callback.
        """
        resp = await self.request('POST', '/verify', verify_request.model_dump(by_alias=True))
        return PaymentVerifyResponse(**resp)

    def payment_url_generator(self, track_id: int) -> str:
        return f"https://gateway.zibal.ir/start/{track_id}"

    async def inquiry(self, inquiry_request: PaymentInquiryRequest) -> PaymentInquiryResponse:
        """
        Inquires the status of a payment based on the trackId.
        """
        resp = await self.request('POST', '/inquiry', inquiry_request.model_dump(by_alias=True))
        return PaymentInquiryResponse(**resp)

    async def callback_verify(self, callback: CallbackParams) -> PaymentVerifyResponse:
        """
        Verifies the payment after the user is redirected to the callback URL.

        Args:
            callback (CallbackParams): The query parameters received in the callback URL.

        Returns:
            PaymentVerifyResponse: The verification result.
        """
        if callback.success != 1:
            raise ValueError("Transaction was not successful (success != 1)")

        verify_data = PaymentVerifyRequest(track_id=callback.track_id)
        return await self.verify(verify_data)

    async def request_lazy_payment(self, payment: PaymentRequest) -> PaymentResponse:
        """
        Initiate a lazy payment request.
        """
        resp = await self.request('POST', '/request/lazy', payment.model_dump(by_alias=True))
        return PaymentResponse(**resp)

    async def verify_lazy_callback(self, callback: LazyCallback) -> PaymentVerifyResponse:
        """
        Verify payment after receiving a Lazy callback.
        Raises ValueError if `success != 1`.
        """
        if callback.success != 1:
            raise ValueError("Lazy transaction was not successful (success != 1)")

        # use same verify endpoint as normal
        verify_req = PaymentVerifyRequest(track_id=callback.track_id)
        return await self.verify(verify_req)
