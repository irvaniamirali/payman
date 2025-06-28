import pytest
from pydantic import ValidationError
from payman.gateways.zibal.models import PaymentRequest


@pytest.mark.asyncio
async def test_payment_request_validation_error():
    with pytest.raises(ValidationError):
        PaymentRequest(
            amount=0,  # Invalid amount
            callback_url="",
            description="",
            order_id="",
            mobile="",
        )
