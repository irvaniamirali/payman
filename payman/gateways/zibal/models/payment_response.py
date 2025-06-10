from typing import Annotated
from pydantic import BaseModel, Field
from ..enums import ZibalResultCode

class PaymentResponse(BaseModel):
    track_id: Annotated[int, Field(alias="trackId", description="Unique identifier for the payment session (used for verification and reporting)")] = ...
    result: Annotated[ZibalResultCode, Field(description="Status code of the payment request")] = ...
    message: Annotated[str, Field(description="Text message explaining the result")] = ...

    model_config = {
        "populate_by_name": True,
        "str_strip_whitespace": True,
        "validate_by_name": True,
        "use_enum_values": True,
    }
