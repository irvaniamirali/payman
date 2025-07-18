import pytest

from payman import Payman
from payman.gateways.zibal.models import PaymentRequest
from pydantic import ValidationError

pay = Payman("zibal", merchant_id="zibal")


@pytest.mark.asyncio
async def test_request_payment_validation_error(mocker):
    with pytest.raises(ValidationError):
        PaymentRequest(
            amount=0,  # Invalid amount
            callback_url="",
            description="",
            order_id="",
            mobile="",
        )
