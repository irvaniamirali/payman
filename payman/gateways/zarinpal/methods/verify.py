from ..models import VerifyRequest, VerifyResponse


class Verify:
    async def verify(self: "ZarinPal", request: VerifyRequest) -> VerifyResponse:
        """
        Verify the transaction status after the payment is complete.

        Args:
            request (VerifyRequest): The verification request.

        Returns:
            VerifyResponse: Verification result including ref_id.
        """
        payload = request.model_dump(mode="json")
        response = await self.client.post("/verify.json", payload)
        return VerifyResponse(**response.get("data"))
