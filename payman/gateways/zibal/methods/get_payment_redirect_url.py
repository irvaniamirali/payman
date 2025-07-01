class GetPaymentRedirectUrl:
    def get_payment_redirect_url(self: "Zibal", track_id: int) -> str:
        """
        Generate a user payment URL for redirecting to Zibal gateway.

        Args:
        track_id (int): Track ID received from `payment()` or `lazy_payment()`.

        Returns:
        str: Full redirect URL to Zibal payment page.
        """
        return f"{self.BASE_URL}/start/{track_id}"
