import pytest
from unittest.mock import AsyncMock
from payman import ZarinPal
from payman.gateways.zarinpal.models import PaymentRequest
from payman.errors import PaymentGatewayError


@pytest.mark.asyncio
async def test_payment_failure_mocked(mocker):
    """
    Test that payment failure raises PaymentGatewayError
    """
    gateway = ZarinPal(merchant_id="test-merchant")

    # Mock the payment method to raise an error
    mocker.patch.object(
        gateway,
        "payment",
        AsyncMock(side_effect=PaymentGatewayError("Mocked payment failure"))
    )

    request = PaymentRequest(
        amount=10000,
        callback_url="https://yourapp.com/callback",
        description="Test payment error"
    )

    with pytest.raises(PaymentGatewayError, match="Mocked payment failure"):
        await gateway.payment(request)
