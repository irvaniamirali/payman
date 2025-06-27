from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from ...interface import CallbackBase
from ..enums import Status


class CallbackParams(BaseModel, CallbackBase):
    track_id: int = Field(..., description="Transaction ID from callback")
    success: int = Field(..., description="1 = success, 0 = failure")
    order_id: str = Field(...)
    status: Status | int = Field(...)

    def is_successful(self) -> bool:
        return self.success == 1

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
