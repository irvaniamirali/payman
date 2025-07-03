from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from ..enums import ResultCode


class PaymentResponse(BaseModel):
    result: ResultCode = Field(None, description="Payment status code")
    track_id: int = Field(None, description="Unique payment session ID")
    message: str = Field(None, description="Result message")

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        use_enum_values=True,
        alias_generator=to_camel,
    )
