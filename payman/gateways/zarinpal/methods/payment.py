from typing import Any
from ..models import (
    PaymentRequest,
    PaymentResponse,
    PaymentMetadata
)


class Payment:
    async def payment(
            self: "ZarinPal", request: PaymentRequest
    ) -> PaymentResponse:
        """
        Create a payment session and retrieve an authority code.

        Args:
            request (PaymentRequest): The payment request details.

        Returns:
            PaymentResponse: The response containing the authority and status.
        """
        payload = request.model_dump(mode="json")
        payload["metadata"] = self.format_metadata(payload.get("metadata"))
        response = await self.client.post("/request.json", payload)
        return PaymentResponse(**response.get("data"))

    @staticmethod
    def format_metadata(metadata: PaymentMetadata | dict[str, Any] | None) -> list[dict[str, str]]:
        """
        Format metadata into ZarinPal-compliant key/value pairs.

        Args:
            metadata (PaymentMetadata | dict | None): Optional metadata.

        Returns:
            list[dict[str, str]]: Formatted metadata list.
        """
        if not metadata:
            return []

        if isinstance(metadata, dict):
            items = metadata.items()
        else:
            items = metadata.model_dump(exclude_none=True).items()

        return [{"key": str(k), "value": str(v)} for k, v in items]
