from pydantic import BaseModel, Field, constr


class CallbackParams(BaseModel):
    authority: constr(min_length=1) = Field(..., description="Transaction authority code returned by ZarinPal")
    status: constr(pattern="^(OK|NOK)$") = Field(..., description="Transaction status: OK or NOK")
