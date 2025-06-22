from payman.errors.base import PaymentGatewayError

class ZibalError(PaymentGatewayError):
    """Base class for all ZarinPal errors."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class MerchantNotFoundError(ZibalError):
    """Merchant not found."""
    pass

class MerchantInactiveError(ZibalError):
    """Merchant is inactive."""
    pass

class InvalidMerchantError(ZibalError):
    """Invalid merchant."""
    pass

class AmountTooLowError(ZibalError):
    """Amount must be greater than 1,000 IRR."""
    pass

class InvalidCallbackUrlError(ZibalError):
    """Invalid callback URL."""
    pass

class AmountExceedsLimitError(ZibalError):
    """Transaction amount exceeds the limit."""
    pass

class InvalidNationalCodeError(ZibalError):
    """Invalid national code."""
    pass

class AlreadyConfirmedError(ZibalError):
    """Already confirmed."""
    pass

class PaymentNotSuccessfulError(ZibalError):
    """Payment order is not successful or unpaid."""
    pass

class InvalidTrackIdError(ZibalError):
    """Invalid track ID."""
    pass


ZIBAL_ERROR_CODE_MAPPING = {
    102: MerchantNotFoundError,
    103: MerchantInactiveError,
    104: InvalidMerchantError,
    105: AmountTooLowError,
    106: InvalidCallbackUrlError,
    113: AmountExceedsLimitError,
    114: InvalidNationalCodeError,
    201: AlreadyConfirmedError,
    202: PaymentNotSuccessfulError,
    203: InvalidTrackIdError,
}
