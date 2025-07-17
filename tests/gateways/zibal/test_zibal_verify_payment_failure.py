import pytest
from unittest.mock import AsyncMock

from payman import Payman
from payman.gateways.zibal.errors import PaymentNotSuccessfulError

pay = Payman("zibal", merchant_id="...")


@pytest.mark.asyncio
async def test_verify_unsuccessful_payment_raises(mocker):
    mocker.patch.object(
        pay, "verify", AsyncMock(side_effect=PaymentNotSuccessfulError("Payment failed"))
    )

    with pytest.raises(PaymentNotSuccessfulError):
        await pay.verify(track_id=99999999)
