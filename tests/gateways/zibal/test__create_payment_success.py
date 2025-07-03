import pytest
from unittest.mock import AsyncMock
from payman import Zibal
from payman.gateways.zibal.models import PaymentRequest, PaymentResponse
from payman.gateways.zibal.enums import ResultCode


@pytest.mark.asyncio
async def test_zibal_create_payment_success(mocker):
    gateway = Zibal(merchant_id="zibal")

    # Define mock response
    mock_response = PaymentResponse(
        result=ResultCode.SUCCESS,
        track_id=123456
    )

    # Patch the `payment` method of the gateway instance
    mocker.patch.object(gateway, "payment", AsyncMock(return_value=mock_response))

    # Prepare the request
    request = PaymentRequest(
        amount=10000,
        callback_url="https://yourapp.com/callback",
        description="Test payment",
        order_id="order-test-001",
        mobile="09121234567",
    )

    # Act
    response = await gateway.payment(request)

    # Assert
    assert response.result == ResultCode.SUCCESS
    assert response.track_id == 123456
