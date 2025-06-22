from typing import Any, Dict
from payman.http import API
from payman.unified import Asyncifiable
from payman.gateways.interface import GatewayInterface
from payman.errors.manager import PaymentGatewayManager
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


class Zibal(GatewayInterface, Asyncifiable):
    """
    Zibal Payment Gateway Client.
    """
    def __init__(self, merchant: str, version: int = 1, **client_params):
        """
        :param merchant: Zibal merchant identifier
        :param version: API version (defaults to v1)
        :param client_params: Additional parameters for the API client.
        """
        self.merchant = merchant
        self.base_url = f"https://gateway.zibal.ir/v{version}"
        self.client = API(base_url=self.base_url, **client_params)

    async def request(self, method: str, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core HTTP method wrapper adding merchant to JSON body.
        """
        data = {"merchant": self.merchant, **payload}
        response = await self.client.request(method, endpoint, json=data)
        if response.get("result") != 100:
            error_code = response["result"]
            error_message = response["message"]
            raise PaymentGatewayManager.handle_error("Zibal", error_code, error_message)
        return response

    async def payment(self, request: PaymentRequest) -> PaymentResponse:
        """
        Creates a new payment session.

        This method sends a payment request to the Zibal API and returns the response containing
        the payment details, including the track ID.

        :param request: An instance of PaymentRequest model containing the payment details.
        :return: An instance of PaymentResponse containing the response data.
        """
        response = await self.request("POST", "/request", request.model_dump(by_alias=True))
        return PaymentResponse(**response)

    def payment_url_generator(self, track_id: int) -> str:
        """
        Generates a URL to redirect the user to the Zibal payment page.

        This method creates a payment URL using the provided track ID, which can be used
        to display the payment page and initiate the payment process.

        :param track_id: The unique identifier for the payment session.
        :return: A string containing the URL to the Zibal payment page.
        """
        return f"https://gateway.zibal.ir/start/{track_id}"

    async def verify(self, request: PaymentVerifyRequest) -> PaymentVerifyResponse:
        """
        Confirms the success of a payment and ends a payment session.

        This method uses the provided track ID to verify the payment status with the Zibal API.
        It should be called after a payment session to ensure that the payment was successful.

        :param request: An instance of PaymentVerifyRequest containing the track_id for verification.
        :return: An instance of PaymentVerifyResponse containing the result of the verification.
        """
        response = await self.request("POST", "/verify", request.model_dump(by_alias=True))
        return PaymentVerifyResponse(**response)

    async def inquiry(self, request: PaymentInquiryRequest) -> PaymentInquiryResponse:
        """
        Inquires about an existing payment session.

        This method allows you to check the status of a payment and retrieve a report
        for a specific payment session using the provided request details.

        :param request: An instance of PaymentInquiryRequest containing the necessary information to perform the inquiry.
        :return: An instance of PaymentInquiryResponse containing the results of the inquiry.
        """
        response = await self.request("POST", "/inquiry", request.model_dump(by_alias=True))
        return PaymentInquiryResponse(**response)

    async def lazy_payment(self, request: PaymentRequest) -> PaymentResponse:
        """
        Initiates a lazy payment without requiring user interaction.

        This method sends the order information to the Zibal system for processing.
        Zibal will send the payment information for the order to the registered callback_url
        when the status changes.

        In the lazy method, this information is sent as JSON via a POST request to the callback_url.
        To finalize the payment session for an order upon successful payment, make sure to
        confirm the received information through the payment confirmation endpoint.

        :param request: An instance of PaymentRequest containing the order details.
        :return: An instance of PaymentResponse containing the result of the payment initiation.
        """
        response = await self.request("POST", "/request/lazy", request.model_dump(by_alias=True))
        return PaymentResponse(**response)
