from typing import Annotated
from pydantic import BaseModel, Field

class PaymentInquiryResponse(BaseModel):
    result: Annotated[int, Field(description="Status code")] = ...
    message: Annotated[str, Field(description="Status message")] = ...
    amount: Annotated[int | None, Field(default=None, description="Transaction amount")] = None
    status: Annotated[int | None, Field(default=None, description="Payment status (e.g., 1: success, 2: canceled)")] = None
    paid_at: Annotated[str | None, Field(default=None, alias="paidAt", description="Payment timestamp (ISO 8601)")] = None
    track_id: Annotated[int, Field(alias="trackId", description="Transaction ID")] = ...

    model_config = {
        "populate_by_name": True,
    }
