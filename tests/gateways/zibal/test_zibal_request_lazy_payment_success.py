import pytest
from unittest.mock import AsyncMock

from payman import Payman
from payman.gateways.zibal.models import PaymentResponse
from payman.gateways.zibal.enums import ResultCode

pay = Payman("zibal", merchant_id="zibal")


@pytest.mark.asyncio
async def test_request_lazy_payment_success(mocker):
    response = PaymentResponse(
        result=ResultCode.SUCCESS,
        track_id=1234567890,
        message="Success Payment"
    )
    mocker.patch.object(pay, "payment", AsyncMock(return_value=response))

    res = await pay.payment(
        amount=10000,
        callback_url="https://example.com/callback",
        description="Test lazy payment",
        order_id="order-test-001",
        mobile="09121234567",
    )

    assert res.success == True
    assert res.result == ResultCode.SUCCESS
    assert res.track_id == 1234567890
    assert res.payment_url == f"https://gateway.zibal.ir/start/{res.track_id}"
    assert res.message == "Success Payment"
