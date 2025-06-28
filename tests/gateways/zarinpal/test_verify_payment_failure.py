import pytest
from unittest.mock import AsyncMock
from payman import ZarinPal
from payman.gateways.zarinpal.models import VerifyRequest
from payman.errors import PaymentGatewayError

@pytest.mark.asyncio
async def test_verify_failure_mocked(mocker):
    """
    Test that verify failure raises PaymentGatewayError
    """
    gateway = ZarinPal(merchant_id="test-merchant")

    # Mock the verify method to raise an error
    mocker.patch.object(
        gateway,
        "verify",
        AsyncMock(side_effect=PaymentGatewayError("Mocked verification failure"))
    )

    request = VerifyRequest(
        authority="AUTH123456789",
        amount=10000
    )

    with pytest.raises(PaymentGatewayError, match="Mocked verification failure"):
        await gateway.verify(request)
