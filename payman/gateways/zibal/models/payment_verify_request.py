from pydantic import BaseModel, Field
from typing import Annotated


class PaymentVerifyRequest(BaseModel):
    track_id: Annotated[int, Field(..., alias="trackId", description="Transaction ID returned by Zibal")]

    model_config = {
        "populate_by_name": True,
    }
