import pytest
from unittest.mock import AsyncMock
from payman import ZarinPal
from payman.gateways.zarinpal.models import PaymentRequest
from payman.errors import PaymentGatewayError


@pytest.mark.asyncio
async def test_create_payment_failure(mocker):
    gateway = ZarinPal(merchant_id="test-merchant")

    mocker.patch.object(
        gateway, "payment", AsyncMock(side_effect=PaymentGatewayError("Payment initiation failed"))
    )

    request = PaymentRequest(
        amount=10000,
        callback_url="https://yourapp.com/callback",
        description="Test payment"
    )

    with pytest.raises(PaymentGatewayError):
        await gateway.payment(request)
