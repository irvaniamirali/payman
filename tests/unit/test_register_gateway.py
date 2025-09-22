import pytest

from payman.core.gateways.register_gateway import register_gateway, get_gateway_instance


class DummyGateway:
    def __init__(self, token):
        self.token = token


def test_register_and_get_gateway():
    register_gateway("dummy", "tests.unit.test_register_gateway.DummyGateway")
    gw = get_gateway_instance("dummy", token="123")
    assert isinstance(gw, DummyGateway)
    assert gw.token == "123"


def test_unknown_gateway():
    with pytest.raises(ValueError):
        get_gateway_instance("unknown")
