from ..models import PaymentRequest, PaymentResponse


class Payment:
    async def payment(
            self: "ZarinPal", request: PaymentRequest
    ) -> PaymentResponse:
        """
        Initiate a new payment request.

        Args:
            request (PaymentRequest): Payment input parameters.

        Returns:
            PaymentResponse: Contains result code and track ID.
        """
        payload = request.model_dump(by_alias=True, mode="json")
        response = await self.client.post("/request", payload)
        return PaymentResponse(**response)
