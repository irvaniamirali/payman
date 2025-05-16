from pydantic import BaseModel, Field, HttpUrl, constr, conint
from typing import Optional, Dict, Union

class PaymentMetadata(BaseModel):
    mobile: Optional[constr(pattern=r"^09\d{9}$")] = None
    order_id: Optional[str] = None

class Payment(BaseModel):
    # merchant_id: constr(min_length=36, max_length=36)
    amount: conint(ge=1)
    currency: Optional[str] = Field(default="IRR", pattern=r"^(IRR|IRT)$")
    description: str
    callback_url: HttpUrl
    metadata: Optional[Union[PaymentMetadata, Dict[str, Union[str, int]]]] = None
