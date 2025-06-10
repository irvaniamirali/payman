from pydantic import BaseModel, Field
from typing import Annotated


class PaymentInquiryRequest(BaseModel):
    track_id: Annotated[int, Field(..., alias="trackId", description="Transaction ID")] = ...

    class Config:
        validate_by_name = True
