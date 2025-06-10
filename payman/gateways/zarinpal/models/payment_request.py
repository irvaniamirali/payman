from pydantic import BaseModel, Field, HttpUrl, constr, conint
from typing import Dict

class PaymentMetadata(BaseModel):
    mobile: constr(pattern=r"^09\d{9}$") | None = None
    order_id: str | None = None

class PaymentRequest(BaseModel):
    amount: conint(ge=1000)
    currency: str = Field(default="IRR", pattern=r"^(IRR|IRT)$")
    description: str
    callback_url: HttpUrl
    metadata: PaymentMetadata | Dict[str, str | int] | None = None
