from ..models import VerifyRequest, VerifyResponse
from payman.utils import parse_input


class Verify:
    async def verify(
        self: "Zibal",
        params: VerifyRequest | dict | None = None,
        **kwargs,
    ) -> VerifyResponse:
        """
        Verify the payment after the user is redirected back to your site.

        Args:
            params (VerifyRequest | dict, optional): Verification input containing the `track_id`.
                Can be passed as a Pydantic model,
                dictionary, or directly via keyword arguments.

        Returns:
            VerifyResponse: Verification result with transaction details.

        Example:
            >>> from payman import Payman
            >>> pay = Payman("zibal", merchant_id="...")
            >>> res = await pay.verify(
            ...     track_id="A1B2C3D4",
            ... )
            >>> if res.success:
            ...     print("Payment was successful.")
            ... else:
            ...     print("Payment failed or was not verified. error message: ", res.message)
        """
        parsed = parse_input(params, VerifyRequest, **kwargs)
        response = await self.client.post(
            "/verify", parsed.model_dump(by_alias=True, mode="json")
        )
        return VerifyResponse(**response)
