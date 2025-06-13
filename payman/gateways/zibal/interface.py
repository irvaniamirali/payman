from ...interface import (
    PaymentRequestor,
    PaymentVerifier,
    PaymentURLGenerator,
    PaymentInquirer,
    CallbackVerifier,
    LazyPaymentRequestor,
    LazyCallbackVerifier
)
from .models import (
    CallbackParams,
    LazyCallback,
    PaymentInquiryRequest,
    PaymentInquiryResponse,
    PaymentRequest,
    PaymentResponse,
    PaymentVerifyRequest,
    PaymentVerifyResponse,
)

class GatewayInterface(
    PaymentRequestor[PaymentRequest, PaymentResponse],
    PaymentVerifier[PaymentVerifyRequest, PaymentVerifyResponse],
    PaymentURLGenerator,
    PaymentInquirer[PaymentInquiryRequest, PaymentInquiryResponse],
    CallbackVerifier[CallbackParams, PaymentVerifyResponse],
    LazyPaymentRequestor[PaymentRequest, PaymentResponse],
    LazyCallbackVerifier[LazyCallback, PaymentVerifyResponse]
):
    pass
