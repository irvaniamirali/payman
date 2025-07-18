import pytest
from unittest.mock import AsyncMock

from payman import Payman
from payman.gateways.zarinpal.models import VerifyResponse, CallbackParams
from payman.gateways.zarinpal.enums import Status

pay = Payman("zarinpal", merchant_id="test-merchant")


@pytest.mark.asyncio
async def test_verify_payment_success(mocker):

    # Simulate a callback (this would normally come from query params)
    authority = "AUTH123456789"
    callback = CallbackParams(authority=authority, status="OK")

    # Mock the verify response (authority is NOT a field here)
    mock_response = VerifyResponse(
        ref_id=12345,
        card_pan="123456******1234",
        fee_type="Merchant",
        fee=10000,
        code=Status.SUCCESS,
        message="Success Payment",
        card_hash="Test Card Hash"
    )

    # Patch the gateway.verify method
    mocker.patch.object(
        pay, "verify", AsyncMock(return_value=mock_response)
    )

    # Simulate verifying the payment
    if callback.is_success:
        response = await pay.verify(authority=callback.authority, amount=10000)
        assert response.ref_id == 12345
        assert response.success == True
        assert response.fee_type == "Merchant"
