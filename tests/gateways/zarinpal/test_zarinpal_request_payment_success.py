import pytest
from unittest.mock import AsyncMock

from payman import Payman
from payman.gateways.zarinpal.models import PaymentResponse
from payman.gateways.zarinpal.enums import Status

pay = Payman("zarinpal", merchant_id="test-merchant")


@pytest.mark.asyncio
async def test_request_payment_success(mocker):
    response = PaymentResponse(
        code=Status.SUCCESS,
        message="Success Payment",
        authority="AUTH123456789",
        fee_type="Merchant",
        fee=10000
    )

    mocker.patch.object(pay, "payment", AsyncMock(return_value=response))

    response = await pay.payment(
        amount=10000,
        callback_url="https://yourapp.com/callback",
        description="Test payment"
    )
    assert response.authority == "AUTH123456789"
    assert response.code == Status.SUCCESS
    assert response.success == True
