from pydantic import BaseModel, Field


class PaymentResponse(BaseModel):
    code: int = Field(..., description="Payment status code")
    message: str = Field(..., description="Payment status message")
    authority: str = Field(..., description="Unique transaction ID")
    fee_type: str = Field(..., description="Type of transaction fee")
    fee: int = Field(..., description="Transaction fee amount")
