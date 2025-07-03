from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from ..enums import Status


class UnverifiedTransaction(BaseModel):
    authority: str
    amount: int
    callback_url: HttpUrl
    referer: str | None = None
    date: datetime


class UnverifiedPayments(BaseModel):
    code: Status = Field(..., description="Payment status code")
    message: str = Field(..., description="Payment status message")
    authorities: list[UnverifiedTransaction] = Field(default_factory=list)

    @property
    def success(self) -> bool:
        return self.code == Status.SUCCESS
