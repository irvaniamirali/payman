from payman.gateways import GatewayInterface, register_gateway, create_gateway
from pydantic import BaseModel


class PaymentRequest(BaseModel):
    amount: int


class PaymentResponse(BaseModel):
    url: str
    authority: str


class CallbackData(BaseModel):
    success: int
    authority: str


class VerifyResponse(BaseModel):
    result: int
    message: str
    amount: int


class DummyGateway(GatewayInterface):
    def __init__(self, merchant_id: str):
        self.merchant_id = merchant_id

    async def payment(self, params: PaymentRequest | dict | None = None, **kwargs) -> PaymentResponse:
        return PaymentResponse(url="https://example.com", authority="xyz")

    def get_payment_redirect_url(self, authority: str) -> str:
        return f"https://example.com/start/{authority}"

    async def verify(self, callback_data: CallbackData | dict | None = None, **kwargs) -> VerifyResponse:
        return VerifyResponse(result=100, message="Success", amount=10000)


def test_register_gateway_and_create_instance():
    register_gateway("dummy", DummyGateway)
    gateway = create_gateway("dummy", merchant_id="xyz")
    assert isinstance(gateway, DummyGateway)
    assert gateway.merchant_id == "xyz"
