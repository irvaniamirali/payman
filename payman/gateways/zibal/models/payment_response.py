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

    @property
    def success(self) -> bool:
        return self.result == ResultCode.SUCCESS

    @property
    def payment_url(self) -> str | None:
        """Returns the gateway payment URL to redirect the user, based on track ID."""
        if not self.track_id:
            return None
        return f"https://gateway.zibal.ir/start/{self.track_id}"
