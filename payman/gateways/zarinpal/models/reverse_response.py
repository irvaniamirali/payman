from pydantic import BaseModel, Field


class ReverseResponse(BaseModel):
    code: int = Field(..., description="Payment status code")
    message: str = Field(..., description="Payment status message")
