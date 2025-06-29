from ..models import ReverseRequest, ReverseResponse


class Reverse:
    async def reverse(self: "ZarinPal", request: ReverseRequest) -> ReverseResponse:
        """
        Reverse a pending or unsettled transaction.

        Args:
            request (ReverseRequest): Details of the transaction to reverse.

        Returns:
            ReverseResponse: Result of the reversal process.
        """
        payload = request.model_dump(mode="json")
        response = await self.client.post("/reverse.json", payload)
        return ReverseResponse(**response.get("data"))
