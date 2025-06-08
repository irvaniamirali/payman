from pydantic import BaseModel, Field, HttpUrl, constr, conint
from typing import Optional, Dict, Union, List

class PaymentMetadata(BaseModel):
    mobile: Optional[constr(pattern=r"^09\d{9}$")] = None
    order_id: Optional[str] = None

class Payment(BaseModel):
    amount: conint(ge=1000)
    currency: Optional[str] = Field(default="IRR", pattern=r"^(IRR|IRT)$")
    description: str
    callback_url: HttpUrl
    metadata: Optional[Union[PaymentMetadata, Dict[str, Union[str, int]]]] = None


class PaymentVerify(BaseModel):
    amount: conint(ge=1000)
    authority: str = Field(..., description="Unique transaction identifier")


class PaymentData(BaseModel):
    code: int = Field(..., description="Status code of the payment")
    message: str = Field(..., description="Status message of the payment")
    authority: str = Field(..., description="Unique transaction identifier")
    fee_type: str = Field(..., description="Type of the transaction fee")
    fee: int = Field(..., description="Amount of the transaction fee")


class PaymentResponse(BaseModel):
    data: PaymentData
    errors: List[str] = Field(default_factory=list, description="List of error messages, if any")

    @property
    def code(self):
        return self.data.code

    @property
    def message(self):
        return self.data.message

    @property
    def authority(self):
        return self.data.authority

    @property
    def fee_type(self):
        return self.data.code

    @property
    def fee(self):
        return self.data.fee


class CallbackParams(BaseModel):
    authority: constr(min_length=1) = Field(..., description="Transaction authority code returned by ZarinPal")
    status: constr(pattern="^(OK|NOK)$") = Field(..., description="Transaction status: OK or NOK")


class VerifyPaymentResponse(BaseModel):
    code: int = Field(..., description="Result code of payment verification")
    ref_id: Optional[int] = Field(..., description="Transaction reference ID if payment successful")
    card_pan: Optional[str] = Field(..., description="Masked card number")
    card_hash: Optional[str] = Field(..., description="SHA256 hash of card number")
    fee_type: Optional[str] = Field(..., description="Who pays the fee (buyer or merchant)")
    fee: Optional[int] = Field(..., description="Fee amount charged")
    message: Optional[str] = Field(..., description="Additional message or error detail")
