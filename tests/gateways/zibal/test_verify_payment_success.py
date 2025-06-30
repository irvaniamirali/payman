import pytest
from unittest.mock import AsyncMock
from payman import Zibal
from payman.gateways.zibal.models import VerifyRequest, CallbackParams, VerifyResponse
from payman.gateways.zibal.enums import Status

@pytest.mark.asyncio
async def test_verify_payment_success_mocked(mocker):
    gateway = Zibal(merchant_id="zibal")

    # Mocked CallbackParams
    callback = CallbackParams(
        track_id=123456,
        success=1,
        status=100,
        order_id="order-test-verify"
    )

    # Mocked response from verify
    mock_response = VerifyResponse(
        status=1,
        result=Status.SUCCESS,
        track_id=callback.track_id,
        message="Success Payment",
        paid_at="2025-06-28T15:00:00+03:30",
    )

    # Patch the verify method
    mocker.patch.object(gateway, "verify", AsyncMock(return_value=mock_response))

    # Simulate verification if callback is successful
    if callback.is_successful():
        verify_response = await gateway.verify(VerifyRequest(track_id=callback.track_id))
        assert verify_response.track_id == callback.track_id
        assert verify_response.result == Status.SUCCESS
        assert verify_response.paid_at == "2025-06-28T15:00:00+03:30"
