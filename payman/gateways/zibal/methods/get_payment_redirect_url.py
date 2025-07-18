class GetPaymentRedirectUrl:
    def get_payment_redirect_url(self: "Zibal", track_id: int) -> str:
        """
        Generate the full payment URL to redirect the user to the Zibal gateway.

        This method constructs the redirect URL using the given `track_id` obtained
        from a successful call to `payment()` or `lazy_payment()`. The returned URL
        should be used to redirect the user to Zibal's payment page.

        Args:
            track_id (int): The unique track ID received in the `PaymentResponse`.

        Returns:
            str: A fully qualified URL to redirect the user for payment.

        Example:
            >>> from payman import Payman
            >>> pay = Payman("zibal", merchant_id="...")
            >>> res = await pay.payment(
            ...     amount=10000,
            ...     callback_url="https://yourdomain.com/callback"
            ... )
            >>> url = pay.get_payment_redirect_url(res.track_id)
            >>> print("Redirect user to:", url)
        """
        return f"{self.BASE_URL}/start/{track_id}"
