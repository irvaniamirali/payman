import pytest
from unittest.mock import AsyncMock
from payman import ZarinPal
from payman.gateways.zarinpal.models import VerifyRequest, VerifyResponse, CallbackParams
from payman.gateways.zarinpal.enums import Status


@pytest.mark.asyncio
async def test_zarinpal_verify_payment_success(mocker):
    gateway = ZarinPal(merchant_id="test-merchant")

    # Simulate a callback (this would normally come from query params)
    authority = "AUTH123456789"
    callback = CallbackParams(authority=authority, status="OK")

    # Mock the verify response (authority is NOT a field here)
    mock_response = VerifyResponse(
        ref_id=12345,
        card_pan="123456******1234",
        fee_type="Merchant",
        fee=10000,
        code=Status.SUCCESS
    )

    # Patch the gateway.verify method
    mocker.patch.object(
        gateway,
        "verify",
        AsyncMock(return_value=mock_response)
    )

    # Simulate verifying the payment
    if callback.is_successful:
        response = await gateway.verify(
            VerifyRequest(authority=callback.authority, amount=10000)
        )
        assert response.ref_id == 12345
        assert response.success == True
        assert response.fee_type == "Merchant"
