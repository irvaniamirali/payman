from ..models import VerifyRequest, VerifyResponse
from payman.utils import parse_input


class Verify:
    async def verify(
        self: "ZarinPal", params: VerifyRequest | dict | None = None, **kwargs
    ) -> VerifyResponse:
        """
        Verify the transaction status after the payment is complete.

        Args:
           params (VerifyRequest | dict, optional): Verification input containing the `authority`.
                Can be passed as a Pydantic model,
                dictionary, or directly via keyword arguments.

        Returns:
            VerifyResponse: Verification result including ref_id.

        Example:
            >>> from payman import Payman
            >>> pay = Payman("zarinpal", merchant_id="...")
            >>> res = await pay.verify(
            ...     authority="A1B2C3D4",
            ... )
            >>> if res.success:
            ...     print("Payment was successful.")
            ... else:
            ...     print("Payment failed or was not verified. error message: ", res.message)
        """
        payload = parse_input(params, VerifyRequest, **kwargs).model_dump(mode="json")
        response = await self.client.post("/verify.json", payload)
        return VerifyResponse(**response.get("data"))
