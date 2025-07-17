import pytest
from unittest.mock import AsyncMock

from payman import Payman, GatewayError

pay = Payman("zarinpal", merchant_id="test-merchant")


@pytest.mark.asyncio
async def test_request_payment_raises(mocker):
    # mock error when calling payment (e.g. server returned error)
    mocker.patch.object(
        pay, "payment", AsyncMock(side_effect=GatewayError("Server error"))
    )

    with pytest.raises(GatewayError):
        await pay.payment(
            amount=10000,
            callback_url="https://yourapp.com/callback",
            description="Test payment"
        )
