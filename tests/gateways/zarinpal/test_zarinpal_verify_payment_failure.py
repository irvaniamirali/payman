import pytest
from unittest.mock import AsyncMock

from payman import Payman, GatewayError

pay = Payman("zarinpal", merchant_id="test-merchant")


@pytest.mark.asyncio
async def test_verify_failure_mocked(mocker):
    mocker.patch.object(
        pay,
        "verify",
        AsyncMock(side_effect=GatewayError("Mocked verification failure"))
    )

    with pytest.raises(GatewayError, match="Mocked verification failure"):
        await pay.verify(authority="AUTH123456789", amount=10000)
