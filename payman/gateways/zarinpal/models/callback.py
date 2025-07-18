from pydantic import BaseModel, Field, ConfigDict, constr
from ...interface import CallbackBase


class CallbackParams(BaseModel, CallbackBase):
    authority: constr(min_length=1) = Field(
        ...,
        description="Transaction authority code returned by ZarinPal",
        alias="Authority"
    )
    status: constr(pattern="^(OK|NOK)$") = Field(
        ...,
        description="Transaction status: OK or NOK",
        alias="Status"
    )

    @property
    def is_success(self) -> bool:
        """Check if the payment was marked successful by ZarinPal redirect."""
        return self.status.upper() == "OK"

    model_config = ConfigDict(populate_by_name=True)
