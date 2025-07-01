from ..models import CallbackParams, VerifyResponse


class CallbackVerify:
    async def callback_verify(
            self: "Zibal", callback: CallbackParams
    ) -> VerifyResponse:
        """
        Verify server-to-server callback from Zibal (lazy verification).

        Args:
            callback (CallbackParams): Payload received in Zibal's callback request.

        Returns:
            VerifyResponse: Transaction info and status.
        """
        payload = callback.model_dump(by_alias=True, mode="json")
        response = await self.client.post("/callback/verify", payload)
        return VerifyResponse(**response)

