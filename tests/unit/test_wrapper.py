from payman.core.gateways import wrapper


def test_payman_calls_register(monkeypatch):
    class FakeGateway:
        def __init__(self, foo):
            self.foo = foo

    monkeypatch.setattr(wrapper, "get_gateway_instance", lambda name, **kw: FakeGateway(**kw))
    gw = wrapper.Payman("fake", foo=123)
    assert isinstance(gw, FakeGateway)
    assert gw.foo == 123
