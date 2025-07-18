import pytest
from unittest.mock import AsyncMock

from payman import Payman
from payman.gateways.zibal.models import (
    CallbackParams,
    VerifyResponse
)
from payman.gateways.zibal.enums import ResultCode, TransactionStatus

pay = Payman("zibal", merchant_id="zibal")


@pytest.mark.asyncio
async def test_verify_payment_success(mocker):
    callback = CallbackParams(
        track_id=1234567890,
        success=1,
        status=ResultCode.SUCCESS,
        order_id="order-test-verify"
    )

    # Simulate verify response
    response = VerifyResponse(
        status=TransactionStatus.VERIFIED,
        result=ResultCode.SUCCESS,
        track_id=callback.track_id,
        message="Success Payment",
        paid_at="2025-06-28T15:00:00+03:30",
        amount=10000,
        card_number="1234567890123456",
        ref_number="1234",
        order_id="ABC123"
    )

    mocker.patch.object(pay, "verify", AsyncMock(return_value=response))

    if callback.is_success:
        verify_response = await pay.verify(track_id=callback.track_id)
        assert verify_response.status == TransactionStatus.VERIFIED
        assert verify_response.result == ResultCode.SUCCESS
        assert verify_response.track_id == callback.track_id
        assert verify_response.message == "Success Payment"
        assert verify_response.paid_at == "2025-06-28T15:00:00+03:30"
        assert verify_response.amount == 10000
        assert verify_response.card_number == "1234567890123456"
        assert verify_response.ref_number == "1234"
        assert verify_response.order_id == "ABC123"
