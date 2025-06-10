from pydantic import BaseModel, Field

class RevenueShareVerifyRequest(BaseModel):
    merchant_id: str = Field(..., min_length=36, max_length=36, description="36-char merchant ID")
    authority: str = Field(..., pattern=r"^A[0-9a-zA-Z\-]{35}$", description="Authority code starting with 'A'")
    amount: int = Field(..., gt=0, description="Original transaction amount in IRR")
