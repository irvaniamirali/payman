import pytest
from unittest.mock import AsyncMock, MagicMock

from parspay import ParsPay
from parspay.gateways.zarinpal.gateway import ZarinPal
from parspay.gateways.zarinpal.models import Payment, PaymentResponse, PaymentData
from parspay.gateways.zarinpal.models import PaymentVerify
from parspay.gateways.zarinpal.errors import ZarinPalVerificationError


@pytest.mark.asyncio
async def test_zarinpal_unified_async_call():
    mock_gateway = MagicMock(spec=ZarinPal)

    payment_data = Payment(amount=10000, description="Test payment", callback_url="https://example.com/callback")
    response_data = PaymentResponse(
        data=PaymentData(code=100, message="Success", authority="AUTH123", fee_type="Merchant", fee=0),
        errors=[]
    )
    mock_gateway.create_payment = AsyncMock(return_value=response_data)

    pay = ParsPay(mock_gateway)

    result = await pay.create_payment(payment_data)

    mock_gateway.create_payment.assert_awaited_once_with(payment_data)
    
    assert isinstance(result, PaymentResponse)
    assert result.data.code == 100
    assert result.data.message == "Success"


@pytest.mark.asyncio
async def test_verify_payment_success():
    client = ZarinPal(merchant_id="test-merchant")

    client.request = AsyncMock(
        return_value={
            "code": 100,
            "ref_id": 12345,
            "card_pan": "1234****5678",
            "card_hash": "abcd1234",
            "fee_type": "merchant",
            "fee": 200,
            "message": "Success"
        }
    )

    params = PaymentVerify(authority="auth123", amount=10000)

    result = await client.verify_payment(params)

    assert result.code == 100
    assert result.ref_id == 12345
    assert result.message == "Success"


@pytest.mark.asyncio
async def test_verify_payment_error():
    client = ZarinPal(merchant_id="test-merchant")

    client.request = AsyncMock(
        return_value={
            "code": 200,
            "message": "Invalid payment"
        }
    )

    params = PaymentVerify(authority="auth123", amount=10000)

    with pytest.raises(ZarinPalVerificationError) as exc_info:
        await client.verify_payment(params)

    assert exc_info.value.code == 200
    assert "Invalid payment" in exc_info.value.message
