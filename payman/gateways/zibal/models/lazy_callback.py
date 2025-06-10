from typing import Annotated
from pydantic import BaseModel, Field

class LazyCallback(BaseModel):
    success: Annotated[int, Field(description="1 = success, 0 = failure")] = ...
    track_id: Annotated[int, Field(alias="trackId", description="Tracking ID of payment session")] = ...
    order_id: Annotated[str | None, Field(default=None, alias="orderId", description="Order ID if provided")] = None
    status: Annotated[int, Field(description="Payment status code")] = ...
    card_number: Annotated[str | None, Field(default=None, alias="cardNumber", description="Masked payer card number")] = None
    hashed_card_number: Annotated[str | None, Field(default=None, alias="hashedCardNumber", description="Hashed payer card number")] = None

    model_config = {
        "populate_by_name": True,
    }
