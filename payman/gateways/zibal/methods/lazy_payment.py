from ..models import PaymentRequest, PaymentResponse


class LazyPayment:
    async def lazy_payment(
            self: "Zibal", request: PaymentRequest
    ) -> PaymentResponse:
        """
        Initiate a lazy (delayed verification) payment.

        Args:
            request (PaymentRequest): Payment input parameters.

        Returns:
            PaymentResponse: Result of payment initiation.
        """
        payload = request.model_dump(by_alias=True, mode="json")
        response = await self.client.post("/request/lazy", payload)
        return PaymentResponse(**response)
