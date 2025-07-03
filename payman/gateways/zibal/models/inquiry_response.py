from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from .multiplexing_info import MultiplexingInfo
from ..enums import ResultCode, TransactionStatus


class InquiryResponse(BaseModel):
    result: ResultCode = Field(..., description="API Status code")
    message: str = Field(..., description="Status message")
    ref_number: int = Field(None, description="Reference number")
    paid_at: str = Field(None, description="Payment timestamp (ISO 8601)")
    verified_at: str = Field(None, description="Verification timestamp")
    status: TransactionStatus = Field(None, description="Payment status")
    amount: int = Field(None, description="Transaction amount")
    order_id: str = Field(..., description="Order ID")
    description: str = Field(..., description="Description of the transaction")
    card_number: str = Field(None, description="Card number used for the transaction")
    wage: int = Field(..., description="Wage associated with the transaction")
    created_at: str = Field(..., description="Creation timestamp of the response")
    multiplexingInfos: list[MultiplexingInfo] = []

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        alias_generator=to_camel,
    )

    @property
    def success(self) -> bool:
        return self.result == ResultCode.SUCCESS

    @property
    def already_verified(self) -> bool:
        return self.result == TransactionStatus.VERIFIED
