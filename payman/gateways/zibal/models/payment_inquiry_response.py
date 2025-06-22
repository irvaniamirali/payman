from typing import Annotated
from pydantic import BaseModel, Field

class PaymentInquiryResponse(BaseModel):
    result: Annotated[int, Field(description="Status code")]
    message: Annotated[str, Field(description="Status message")]
    ref_number: Annotated[int | None, Field(alias="refNumber", description="Reference number")]
    paid_at: Annotated[str | None, Field(default=None, alias="paidAt", description="Payment timestamp (ISO 8601)")]
    verified_at: Annotated[str | None, Field(alias="verifiedAt", description="Verification timestamp")]
    status: Annotated[int | None, Field(default=None, description="Payment status (e.g., 1: success, 2: canceled)")]
    amount: Annotated[int | None, Field(default=None, description="Transaction amount")]
    order_id: Annotated[str, Field(alias="orderId", description="Order ID")]
    description: Annotated[str, Field(description="Description of the transaction")]
    card_number: Annotated[str | None, Field(alias="cardNumber", description="Card number used for the transaction")]
    wage: Annotated[int, Field(description="Wage associated with the transaction")]
    created_at: Annotated[str, Field(alias="createdAt", description="Creation timestamp of the response")]

    model_config = {
        "populate_by_name": True,
    }
