from ..models import UnverifiedPayments


class GetUnverifiedPayments:
    async def get_unverified_payments(self: "ZarinPal") -> UnverifiedPayments:
        """
        Fetch the list of successful but not-yet-verified payments from ZarinPal.

        Returns:
            UnverifiedPayments: Contains status code, message, and a list of unverified transactions.
        """
        response = await self.client.post("/unVerified.json")
        return UnverifiedPayments(**response.get("data"))
