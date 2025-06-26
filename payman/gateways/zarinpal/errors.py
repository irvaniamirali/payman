from payman.errors.base import PaymentGatewayError

class ZarinPalError(PaymentGatewayError):
    """Base class for all ZarinPal errors."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class ValidationError(ZarinPalError):
    """Raised for validation errors."""
    pass

class TerminalError(ZarinPalError):
    """Raised for terminal-related errors."""
    pass

class PaymentError(ZarinPalError):
    """Raised for payment-related errors."""
    pass

class MerchantIDError(ZarinPalError):
    """Raised when the merchant ID is invalid."""
    pass

class SessionError(ZarinPalError):
    """Raised for session-related errors."""
    pass

class AuthorityError(ZarinPalError):
    """Raised for authority-related errors."""
    pass

class ReverseError(ZarinPalError):
    """Raised for errors related to reversing transactions."""
    pass


ZARINPAL_ERRORS = {
    -9: ValidationError,
    -10: MerchantIDError,
    -11: TerminalError,
    -12: PaymentError,
    -15: TerminalError,
    -16: TerminalError,
    -17: TerminalError,
    -18: PaymentError,
    -19: PaymentError,
    -30: PaymentError,
    -31: PaymentError,
    -32: PaymentError,
    -33: PaymentError,
    -34: PaymentError,
    -35: PaymentError,
    -36: PaymentError,
    -37: PaymentError,
    -38: PaymentError,
    -39: PaymentError,
    -40: PaymentError,
    -41: PaymentError,
    -50: SessionError,
    -51: SessionError,
    -52: ZarinPalError,
    -53: SessionError,
    -54: AuthorityError,
    -55: SessionError,
    -60: ReverseError,
    -61: ReverseError,
    -62: ReverseError,
    -63: ReverseError,
}
