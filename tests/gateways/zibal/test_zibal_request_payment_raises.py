import pytest
from unittest.mock import AsyncMock

from payman import Payman, GatewayError

pay = Payman("zibal", merchant_id="zibal")


@pytest.mark.asyncio
async def test_request_payment_raises(mocker):
    # mock error when calling payment (e.g. server returned error)
    mocker.patch.object(
        pay, "payment", AsyncMock(side_effect=GatewayError("Server error"))
    )

    with pytest.raises(GatewayError):
        await pay.payment(
            amount=10000,
            callback_url="https://example.com/callback",
            description="Test payment",
            order_id="order-test-001",
            mobile="09121234567",
        )

