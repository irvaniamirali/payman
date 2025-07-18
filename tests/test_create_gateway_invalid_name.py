import pytest
from payman.gateways import create_gateway


def test_create_gateway_invalid_name():
    with pytest.raises(ValueError) as exc:
        create_gateway("unknown_gateway")
    assert "not supported" in str(exc.value)
