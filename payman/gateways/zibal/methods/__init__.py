from .callback_verify import CallbackVerify
from .get_payment_redirect_url import GetPaymentRedirectUrl
from .inquiry import Inquiry
from .lazy_payment import LazyPayment
from .payment import Payment
from .verify import Verify


class Methods(
    CallbackVerify,
    GetPaymentRedirectUrl,
    Inquiry,
    LazyPayment,
    Payment,
    Verify
):
    pass
