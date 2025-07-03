from pydantic import BaseModel, Field
from ..enums import Status


class ReverseResponse(BaseModel):
    code: Status = Field(..., description="Payment status code")
    message: str = Field(..., description="Payment status message")

    @property
    def success(self) -> bool:
        return self.code == Status.SUCCESS
