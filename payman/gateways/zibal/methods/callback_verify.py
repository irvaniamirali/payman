from ..models import CallbackParams, VerifyResponse
from payman.utils import parse_input


class CallbackVerify:
    async def callback_verify(
        self: "Zibal", callback: CallbackParams | dict | None = None, **kwargs
    ) -> VerifyResponse:
        """
        Verify the server-to-server callback notification from Zibal for lazy payment verification.

        This method is used to confirm the payment result after Zibal sends a callback
        to your server, typically in delayed verification scenarios.

        Args:
            callback (CallbackParams | dict | None): Payload received from Zibal in the callback request.
                This can be a Pydantic model (`CallbackParams`), a dictionary, or None. If `None`,
                the method will raise an error.

        Returns:
            VerifyResponse: Contains detailed information about the transaction verification status.

        Example:
            >>> from payman import Payman
            >>> pay = Payman("zibal", merchant_id="...")
            >>> # Imagine 'callback_data' is a dict received from Zibal's HTTP callback request
            >>> callback_data = {
            ...     "track_id": 123456,
            ...     "result": 100,
            ...     # ... other fields ...
            ... }
            >>> callback_params = CallbackParams(**callback_data)
            >>> response = await pay.callback_verify(callback_params)
            >>> if response.success:
            ...     print("Callback verification succeeded.")
            ... else:
            ...     print("Callback verification failed.")
        """
        parsed = parse_input(callback, CallbackParams, **kwargs)
        response = await self.client.post(
            "/callback/verify", parsed.model_dump(by_alias=True, mode="json")
        )
        return VerifyResponse(**response)
