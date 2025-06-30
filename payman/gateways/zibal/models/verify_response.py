from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from .multiplexing_info import MultiplexingInfo


class VerifyResponse(BaseModel):
    result: int = Field(
        ..., description="Gateway response status code. 100 means success."
    )
    message: str = Field(..., description="Text message explaining the result.")
    amount: int | None = Field(None, description="Paid amount in Rial")
    status: int | None = Field(
        None, description="Bank transaction status (1: success, 2: canceled)"
    )
    paid_at: str | None = Field(
        None, description="Payment timestamp in ISO 8601 format"
    )
    card_number: str | None = Field(
        None, description="Masked card number used for payment"
    )
    ref_number: str | None = Field(None, description="Bank reference number")
    order_id: str | None = Field(None, description="Optional merchant order ID")
    description: str | None = None
    track_id: int | None = Field(None, description="Zibal transaction tracking ID")
    multiplexingInfos: list[MultiplexingInfo] = []

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
