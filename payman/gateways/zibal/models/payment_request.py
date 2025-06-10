from pydantic import BaseModel, Field, conint, constr
from typing import List, Annotated


class PaymentRequest(BaseModel):
    amount: Annotated[
        conint(ge=1000, le=500_000_000),
        Field(description="Total order amount in IRR")
    ]

    callback_url: Annotated[
        str,
        Field(alias="callbackUrl", max_length=2048, description="URL to redirect after payment")
    ]

    description: Annotated[
        str | None,
        Field(default=None, max_length=255, description="Optional description shown in reports")
    ]

    order_id: Annotated[
        str | None,
        Field(default=None, alias="orderId", max_length=255, description="Unique order ID")
    ]

    mobile: Annotated[
        constr(min_length=10, max_length=13) | None,
        Field(default=None, description="Mobile number to display saved cards")
    ]

    allowed_cards: Annotated[
        List[constr(min_length=16, max_length=16)] | None,
        Field(default=None, alias="allowedCards", description="Allowed card numbers")
    ] = None

    ledger_id: Annotated[
        str | None,
        Field(default=None, alias="ledgerId", description="Ledger ID for balance")
    ] = None

    national_code: Annotated[
        constr(min_length=10, max_length=10) | None,
        Field(default=None, alias="nationalCode", description="10-digit national code")
    ] = None

    check_mobile_with_card: Annotated[
        bool,
        Field(default=False, alias="checkMobileWithCard", description="Match mobile with card")
    ] = None

    model_config = {
        "populate_by_name": True,
        "str_strip_whitespace": True,
    }
