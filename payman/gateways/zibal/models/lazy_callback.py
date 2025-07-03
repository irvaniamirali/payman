from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from ..enums import TransactionStatus

class LazyCallback(BaseModel):
    success: int = Field(..., description="1 = success, 0 = failure")
    track_id: int = Field(..., description="Payment session tracking ID")
    order_id: str = Field(None, description="Order ID if provided")
    status: TransactionStatus = Field(..., description="Payment status code")
    card_number: str = Field(None, description="Masked payer card number")
    hashed_card_number: str = Field(None, description="Hashed payer card number")

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        alias_generator=to_camel,
    )

    @property
    def is_successful(self) -> bool:
        return self.success == 1
