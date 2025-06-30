from pydantic import BaseModel, Field, conint


class VerifyRequest(BaseModel):
    amount: conint(ge=1000)
    authority: str = Field(..., description="Unique transaction identifier")
