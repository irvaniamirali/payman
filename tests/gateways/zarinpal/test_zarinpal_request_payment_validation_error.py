import pytest

from payman import Payman
from payman.gateways.zarinpal.models import PaymentRequest
from pydantic import ValidationError

pay = Payman("zarinpal", merchant_id="zibal")


@pytest.mark.asyncio
async def test_request_payment_validation_error(mocker):
    with pytest.raises(ValidationError):
        PaymentRequest(
            amount=0,  # Invalid amount
            callback_url="",
            description="",
        )
