from pydantic import BaseModel, Field, constr
from ...interface import CallbackBase


class CallbackParams(BaseModel, CallbackBase):
    authority: constr(min_length=1) = Field(
        ..., description="Transaction authority code returned by ZarinPal"
    )
    status: constr(pattern="^(OK|NOK)$") = Field(
        ..., description="Transaction status: OK or NOK"
    )

    def is_successful(self) -> bool:
        """Check if the payment was marked successful by ZarinPal redirect."""
        return self.status.upper() == "OK"
