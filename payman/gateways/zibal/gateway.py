from typing import Any, Dict
from ...http import API
from ...unified import Asyncifiable
from ...interface import BaseGateway
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


class Zibal(BaseGateway, Asyncifiable):
    """
    Zibal Payment Gateway Client
    """
    def __init__(self, merchant: str, version: int = 1, **client_params):
        """
        :param merchant: Zibal merchant identifier
        :param version: API version (defaults to v1)
        """
        self.merchant = merchant
        self.base_url = f"https://gateway.zibal.ir/v{version}"
        self.client = API(base_url=self.base_url, **client_params)

    async def request(self, method: str, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core HTTP method wrapper adding merchant to JSON body.
        """
        data = {"merchant": self.merchant, **payload}
        return await self.client.request(method, endpoint, json=data)

    async def request_payment(self, req: PaymentRequest) -> PaymentResponse:
        """
        Creates a new payment session.

        :param req: PaymentRequest model
        :return: PaymentResponse with track_id, etc.
        """
        data = req.model_dump(by_alias=True)
        resp = await self.request("POST", "/request", data)
        return PaymentResponse(**resp)

    async def verify(self, req: PaymentVerifyRequest) -> PaymentVerifyResponse:
        """
        Confirm payment session given a trackId.

        :param req: PaymentVerifyRequest with track_id
        :return: PaymentVerifyResponse
        """
        resp = await self.request("POST", "/verify", req.model_dump(by_alias=True))
        return PaymentVerifyResponse(**resp)

    def payment_url_generator(self, track_id: int) -> str:
        """
        Returns URL to redirect user to Zibal payment page.
        """
        return f"{self.base_url}start/{track_id}"

    async def inquiry(self, req: PaymentInquiryRequest) -> PaymentInquiryResponse:
        """
        Inquire about existing payment session.
        """
        resp = await self.request("POST", "/inquiry", req.model_dump(by_alias=True))
        return PaymentInquiryResponse(**resp)

    async def callback_verify(self, callback: CallbackParams) -> PaymentVerifyResponse:
        """
        Confirm user payment session after callback URL is hit.

        Raises ValueError if callback indicates failure.
        """
        if callback.success != 1:
            raise ValueError("Callback successful flag is not 1.")
        return await self.verify(PaymentVerifyRequest(track_id=callback.track_id))

    async def request_lazy_payment(self, req: PaymentRequest) -> PaymentResponse:
        """
        Initiates a lazy payment (user doesn't click through).
        """
        resp = await self.request("POST", "/request/lazy", req.model_dump(by_alias=True))
        return PaymentResponse(**resp)

    async def verify_lazy_callback(self, callback: LazyCallback) -> PaymentVerifyResponse:
        """
        Verify lazy callback payload. Same endpoint as standard verify.
        """
        if callback.success != 1:
            raise ValueError("Lazy callback indicates failure.")
        return await self.verify(PaymentVerifyRequest(track_id=callback.track_id))
