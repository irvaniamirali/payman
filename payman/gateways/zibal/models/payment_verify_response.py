from typing import Annotated
from pydantic import BaseModel, Field

class PaymentVerifyResponse(BaseModel):
    result: Annotated[int, Field(description="Status code: 100 means success")] = ...
    message: Annotated[str, Field(description="Status message")] = ...
    amount: Annotated[int | None, Field(default=None, description="Paid amount in Rial")] = None
    status: Annotated[int | None, Field(default=None, description="Payment status (e.g., 1: success, 2: canceled)")] = None
    paid_at: Annotated[str | None, Field(default=None, alias="paidAt", description="Payment timestamp (ISO 8601)")] = None
    card_number: Annotated[str | None, Field(default=None, alias="cardNumber", description="Payer's card number (masked)")] = None
    ref_number: Annotated[str | None, Field(default=None, alias="refNumber", description="Payment reference number")] = None
    order_id: Annotated[str | None, Field(default=None, alias="orderId", description="Optional order ID")] = None
    description: Annotated[str | None, Field(default=None, description="Transaction description")] = None
    track_id: Annotated[int | None, Field(default=None, alias="trackId", description="Transaction ID (if returned)")] = None

    model_config = {
        "populate_by_name": True,
        "validate_by_name": True,
    }
