from pydantic import BaseModel, Field
from ..enums import Status


class PaymentResponse(BaseModel):
    code: Status = Field(..., description="Payment status code")
    message: str = Field(..., description="Payment status message")
    authority: str = Field(..., description="Unique transaction ID")
    fee_type: str = Field(..., description="Type of transaction fee")
    fee: int = Field(..., description="Transaction fee amount")

    @property
    def success(self) -> bool:
        return self.code == Status.SUCCESS

    @property
    def already_verified(self) -> bool:
        return self.code == Status.ALREADY_VERIFIED
