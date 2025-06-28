import pytest
from unittest.mock import AsyncMock
from payman import Zibal
from payman.gateways.zibal.models import PaymentRequest
from payman.errors import PaymentGatewayError


@pytest.mark.asyncio
async def test_payment_gateway_error_mocked(mocker):
    gateway = Zibal(merchant_id="zibal")

    # mock error when calling payment (e.g. server returned error)
    mocker.patch.object(
        gateway, "payment", AsyncMock(side_effect=PaymentGatewayError("Server error"))
    )

    valid_request = PaymentRequest(
        amount=10000,
        callback_url="https://yourapp.com/callback",
        description="Valid payment",
        order_id="order-123",
        mobile="09123456789",
    )

    with pytest.raises(PaymentGatewayError):
        await gateway.payment(valid_request)
