from pydantic import BaseModel, Field, field_validator
from typing import List
from .wage import Wage

class RevenueShareRequest(BaseModel):
    merchant_id: str = Field(..., min_length=36, max_length=36, description="36-char merchant ID")
    amount: int = Field(..., gt=0, description="Total transaction amount in IRR")
    callback_url: str = Field(..., description="URL to redirect buyer after payment")
    description: str = Field(..., max_length=500, description="Transaction description")
    wages: List[Wage] = Field(..., description="List of up to 5 revenue-share entries")
    mobile: str | None = Field(None, pattern=r"^09\d{9}$", description="Buyer’s mobile (optional)")
    email: str | None = Field(None, description="Buyer’s email (optional)")
    order_id: str | None = Field(None, description="Order identifier (optional)")

    @field_validator("wages")
    def check_wages_length(cls, v):
        if not (1 <= len(v) <= 5):
            raise ValueError("wages must contain between 1 and 5 items")
        return v
