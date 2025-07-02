

class GetPaymentRedirectUrl:
    def get_payment_redirect_url(self: "ZarinPal", authority: str) -> str:
        """
        Construct the full URL to redirect the user to the payment gateway page.

        Args:
            authority (str): The unique authority or token received from a successful payment initiation.

        Returns:
            str: A complete URL where the customer should be redirected to complete the payment process.
        """
        domain = self._BASE_DOMAIN[self.sandbox]
        return f"https://{domain}/pg/StartPay/{authority}"
