from ..models import InquiryRequest, InquiryResponse
from payman.utils import parse_input


class Inquiry:
    async def inquiry(
        self: "Zibal", params: InquiryRequest | dict | None = None, **kwargs
    ) -> InquiryResponse:
        """
        Inquire the current status of a payment by track ID or order ID.

        This method allows you to check the latest status of a transaction,
        including whether it has been verified, refunded, or still pending.

        Args:
            params (InquiryRequest | dict, optional): Input containing either `track_id`
                or `order_id`. You may provide a Pydantic model, a dictionary,
                or use keyword arguments directly.

        Returns:
            InquiryResponse: Detailed information about the transaction's current state.

        Example:
            >>> from payman import Payman
            >>> from payman.gateways.zibal.enums import TransactionStatus
            >>> pay = Payman("zibal", merchant_id="...")
            >>> res = await pay.inquiry(
            ...     track_id="A1B2C3D4"
            ... )
            >>> if response.status == TransactionStatus.VERIFIED:
            ...     print("Payment has been verified.")
            ... else:
            ...     print("Payment status:", response.status)
        """
        parsed = parse_input(params, InquiryRequest, **kwargs)
        response = await self.client.post(
            "/inquiry", parsed.model_dump(by_alias=True, mode="json")
        )
        return InquiryResponse(**response)
