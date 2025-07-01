from ..models import VerifyRequest, VerifyResponse


class Verify:
    async def verify(
            self: "Zibal", request: VerifyRequest
    ) -> VerifyResponse:
        """
        Verify the payment after redirect or callback.

        Args:
            request (VerifyRequest): Track ID to verify.

        Returns:
            VerifyResponse: Verification result with transaction details.
        """
        payload = request.model_dump(by_alias=True, mode="json")
        response = await self.client.post("/verify", payload)
        return VerifyResponse(**response)
