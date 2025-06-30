from pydantic import BaseModel, Field


class Wage(BaseModel):
    iban: str = Field(
        ..., pattern=r"^IR[0-9]{24}$", description="26-char IBAN starting with IR"
    )
    amount: int = Field(..., gt=0, description="Split amount in IRR")
    description: str = Field(
        ..., max_length=500, description="Description of this split"
    )


class WageResponse(Wage): ...
