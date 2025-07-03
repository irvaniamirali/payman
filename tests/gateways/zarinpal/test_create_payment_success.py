import pytest
from unittest.mock import AsyncMock
from payman import ZarinPal
from payman.gateways.zarinpal.models import PaymentRequest, PaymentResponse
from payman.gateways.zarinpal.enums import Status


@pytest.mark.asyncio
async def test_zarinpal_create_payment_success(mocker):
    gateway = ZarinPal(merchant_id="test-merchant")

    mock_response = PaymentResponse(
        code=Status.SUCCESS,
        message="Success",
        authority="AUTH123456789",
        fee_type="Merchant",
        fee=10000
    )

    mocker.patch.object(gateway, "payment", AsyncMock(return_value=mock_response))

    request = PaymentRequest(
        amount=10000,
        callback_url="https://yourapp.com/callback",
        description="Test payment"
    )

    response = await gateway.payment(request)
    assert response.authority == "AUTH123456789"
    assert response.code == Status.SUCCESS
    assert response.success == True
