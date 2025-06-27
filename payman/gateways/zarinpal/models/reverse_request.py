from pydantic import BaseModel, Field


class ReverseRequest(BaseModel):
    authority: str = Field(..., description="Unique transaction ID")
