from pydantic import BaseModel, ConfigDict, HttpUrl, constr, conint, Field
from pydantic.alias_generators import to_camel
from typing import List, Literal
from .multiplexing_info import MultiplexingInfo


class PaymentRequest(BaseModel):
    amount: conint(ge=100)
    callback_url: HttpUrl
    description: str = None
    order_id: str = None
    mobile: constr(min_length=11, max_length=11, pattern=r"^09\d{9}$") = None
    allowed_cards: List[constr(min_length=16, max_length=16, pattern=r"^\d{16}$")] = (
        None
    )
    ledger_id: str = None
    national_code: constr(min_length=10, max_length=10, pattern=r"^\d{10}$") = None
    check_mobile_with_card: bool = None
    percent_mode: Literal[0, 1] = 0
    fee_mode: Literal[0, 1, 2] = 0
    multiplexingInfos: list[MultiplexingInfo] = []

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
