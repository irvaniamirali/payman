from pydantic import BaseModel, Field
from typing import List


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
