from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class LazyCallback(BaseModel):
    success: int = Field(..., description="1 = success, 0 = failure")
    track_id: int = Field(..., description="Payment session tracking ID")
    order_id: str = Field(None, description="Order ID if provided")
    status: int = Field(..., description="Payment status code")
    card_number: str = Field(None, description="Masked payer card number")
    hashed_card_number: str = Field(None, description="Hashed payer card number")

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
