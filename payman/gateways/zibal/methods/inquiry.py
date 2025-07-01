from ..models import InquiryRequest, InquiryResponse


class Inquiry:
    async def inquiry(
            self: "Zibal", request: InquiryRequest
    ) -> InquiryResponse:
        """
        Inquire the current state of a payment.

        Args:
            request (InquiryRequest): Track ID or order ID.

        Returns:
            InquiryResponse: Current status and transaction details.
        """
        payload = request.model_dump(by_alias=True, mode="json")
        response = await self.client.post("/inquiry", payload)
        return InquiryResponse(**response)
