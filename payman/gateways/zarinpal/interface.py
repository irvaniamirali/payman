from ...interface import (
    PaymentRequestor,
    PaymentVerifier,
    PaymentURLGenerator
)
from .models import (
    PaymentRequest,
    PaymentResponse,
    PaymentVerifyRequest,
    PaymentVerifyResponse,
)

class GatewayInterface(
    PaymentRequestor[PaymentRequest, PaymentResponse],
    PaymentVerifier[PaymentVerifyRequest, PaymentVerifyResponse],
    PaymentURLGenerator,
):
    pass
