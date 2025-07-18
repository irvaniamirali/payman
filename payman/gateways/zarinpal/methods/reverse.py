from ..models import ReverseRequest, ReverseResponse
from payman.utils import parse_input


class Reverse:
    async def reverse(
        self: "ZarinPal", params: ReverseRequest | dict | None = None, **kwargs
    ) -> ReverseResponse:
        """
        Reverses a pending or unsettled transaction in ZarinPal.

        This method is used when a payment session has not yet been settled,
        and you want to cancel or refund it before it's finalized by ZarinPal.

        Args:
            params (ReverseRequest | dict | None): Details of the transaction to be reversed.
                You can provide:
                - A `ReverseRequest` Pydantic model
                - A plain dictionary with equivalent fields
                - Or keyword arguments (`**kwargs`) matching the model fields

        Returns:
            ReverseResponse: Contains information about the reversal status and messages.

        Example:
            >>> from payman import Payman
            >>> pay = Payman("zarinpal", merchant_id="...")
            >>> res = await pay.reverse(
            ...     authority="A00000000000000000000000000123456789",
            ...     amount=10000
            ... )
            >>> if response.success:
            ...     print("Transaction reversed successfully!")
            ... else:
            ...     print("Reversal failed:", response.message)
        """
        payload = parse_input(params, ReverseRequest, **kwargs).model_dump(mode="json")
        response = await self.client.post("/reverse.json", payload)
        return ReverseResponse(**response.get("data"))
