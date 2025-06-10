from pydantic import BaseModel, Field

class RevenueShareResponse(BaseModel):
    code: int = Field(..., description="Status code (100 = success, others = errors)")
    message: str = Field(..., description="API status message")
    authority: str = Field(..., description="Unique transaction reference for redirect")
    fee_type: str = Field(..., description="Fee bearer: Merchant or Buyer")
    fee: int = Field(..., description="Fee amount in IRR")
