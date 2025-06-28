import pytest
from unittest.mock import AsyncMock
from payman import Zibal
from payman.gateways.zibal.models import VerifyRequest
from payman.gateways.zibal.errors import PaymentNotSuccessfulError


@pytest.mark.asyncio
async def test_verify_unsuccessful_payment_raises_mocked(mocker):
    gateway = Zibal(merchant_id="zibal")

    mocker.patch.object(
        gateway, "verify", AsyncMock(side_effect=PaymentNotSuccessfulError("Payment failed"))
    )

    with pytest.raises(PaymentNotSuccessfulError):
        await gateway.verify(VerifyRequest(track_id=99999999))
