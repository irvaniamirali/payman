from ..models import PaymentRequest, PaymentResponse
from payman.utils import parse_input


class LazyPayment:
    async def lazy_payment(
        self: "Zibal", params: PaymentRequest | dict | None = None, **kwargs
    ) -> PaymentResponse:
        """
         Initiate a lazy (delayed verification) payment request.

        This method starts the payment process without immediately verifying the result.
        After redirecting the user to the gateway, the verification should happen separately
        using the `lazy_verify` method once the user returns.

        Args:
            params (PaymentRequest | dict, optional): Input payment parameters including `amount`,
                `callback_url`, and optionally `mobile`. Can be passed as a model,
                dictionary, or keyword arguments.

        Returns:
            PaymentResponse: Response containing the payment URL and track ID for redirection.

        Example:
            >>> from payman import Payman
            >>> pay = Payman("zibal", merchant_id="...")
            >>> res = await pay.lazy_payment(
            ...     amount=25000,
            ...     callback_url="https://yourdomain.com/lazy-callback",
            ... )
            >>> print("Redirect the user to:", response.payment_url)
        """
        parsed = parse_input(params, PaymentRequest, **kwargs)
        response = await self.client.post(
            "/request/lazy", parsed.model_dump(by_alias=True, mode="json")
        )
        return PaymentResponse(**response)
