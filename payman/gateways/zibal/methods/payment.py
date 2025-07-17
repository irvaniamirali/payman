from ..models import PaymentRequest, PaymentResponse
from payman.utils import parse_input


class Payment:
    async def payment(
        self: "Zibal",
        params: PaymentRequest | dict | None = None,
        **kwargs,
    ) -> PaymentResponse:
        """
        Initiate a new payment request.

        Args:
            params (PaymentRequest | dict): Payment input parameters.
                Can be passed as a Pydantic model, dictionary, or directly via keyword arguments.

        Returns:
            PaymentResponse: Contains result code and track ID.

        Example:
        >>> from payman import Payman
        >>> pay = Payman("zibal", merchant_id="...")
        >>> res = await pay.payment(
        ...     amount=10000,
        ...     callback_url="https://yourdomain.com/callback",
        ...     mobile="09123456789",
        ... )
        >>> print("Redirect the user to:", res.payment_url)
        """
        parsed = parse_input(params, PaymentRequest, **kwargs)
        response = await self.client.post(
            "/request", parsed.model_dump(by_alias=True, mode="json")
        )
        return PaymentResponse(**response)
