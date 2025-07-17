from typing import Any
from ..models import PaymentRequest, PaymentResponse, PaymentMetadata
from payman.utils import parse_input


class Payment:
    async def payment(
        self: "ZarinPal", params: PaymentRequest | dict | None = None, **kwargs
    ) -> PaymentResponse:
        """
        Initiates a new payment session and retrieves an authority code from ZarinPal.

        You can pass either a `PaymentRequest` model, a dictionary of parameters,
        or individual keyword arguments. The input will be validated automatically.

        Args:
            params (PaymentRequest | dict | None): The payment request details. You can either:
                - Provide a `PaymentRequest` Pydantic model instance.
                - Provide a plain `dict`.
                - Or pass keyword arguments (`**kwargs`).

        Returns:
            PaymentResponse: Contains authority code, status, and other details.

        Example:
            >>> from payman import Payman
            >>> pay = Payman("zarinpal", merchant_id="...")
            >>> res = await pay.payment(
            ...     amount=10000,
            ...     callback_url="https://yourapp.com/callback",
            ...     description="Purchase",
            ...     metadata={"email": "user@example.com", "mobile": "09123456789"}
            ... )
            >>> print(res.authority)
        """
        payload = parse_input(params, PaymentRequest, **kwargs).model_dump(mode="json")
        payload["metadata"] = self.format_metadata(payload.get("metadata"))
        response = await self.client.post("/request.json", payload)
        return PaymentResponse(**response.get("data"))

    @staticmethod
    def format_metadata(metadata: PaymentMetadata | dict[str, Any] | None) -> list[dict[str, str]]:
        """
        Converts metadata to ZarinPal's expected format (list of key-value pairs).

        This helper ensures the metadata is structured as a list of dictionaries
        where each item contains a `key` and `value` string, as required by ZarinPal.

        Args:
            metadata (PaymentMetadata | dict | None): Additional optional metadata fields.
                Can be provided as:
                - A `PaymentMetadata` Pydantic model
                - A plain dictionary

        Returns:
            list[dict[str, str]]: A list of {"key": ..., "value": ...} items for ZarinPal.

        Example:
            >>> Payment.format_metadata({"email": "user@example.com"})
            [{'key': 'email', 'value': 'user@example.com'}]
        """
        if not metadata:
            return []

        if isinstance(metadata, dict):
            items = metadata.items()
        else:
            items = metadata.model_dump(exclude_none=True).items()

        return [{"key": str(k), "value": str(v)} for k, v in items]
