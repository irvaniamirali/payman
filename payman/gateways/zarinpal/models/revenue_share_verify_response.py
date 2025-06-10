from pydantic import BaseModel, Field
from typing import List
from .wage import Wage

class RevenueShareVerifyResponse(BaseModel):
    wages: List[Wage] = Field(..., description="List of splits as sent in the request")
    code: int = Field(..., description="Status code (100 = success, 101 = already verified)")
    message: str = Field(..., description="API status message")
    card_pan: str = Field(..., description="Masked card number")
    card_hash: str = Field(..., description="SHA256 hash of the card")
    ref_id: int = Field(..., description="Unique reference ID of the successful payment")
    fee_type: str = Field(..., description="Fee bearer: Merchant or Buyer")
    fee: int = Field(..., description="Fee amount in IRR")
