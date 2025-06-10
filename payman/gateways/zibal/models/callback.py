from typing import Annotated
from pydantic import BaseModel, Field


class CallbackParams(BaseModel):
    track_id: Annotated[int, Field(alias="trackId", description="Transaction ID from callback")] = ...
    success: Annotated[int, Field(description="1 = success, 0 = failure")] = ...

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "str_strip_whitespace": True,
    }
