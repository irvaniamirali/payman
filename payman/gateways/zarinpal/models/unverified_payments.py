from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime


class UnverifiedTransaction(BaseModel):
    authority: str
    amount: int
    callback_url: HttpUrl
    referer: str | None = None
    date: datetime


class UnverifiedPayments(BaseModel):
    code: int = Field(..., description="Payment status code")
    message: str = Field(..., description="Payment status message")
    authorities: list[UnverifiedTransaction] = Field(default_factory=list)
