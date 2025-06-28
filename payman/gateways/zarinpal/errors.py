from payman.errors.base import PaymentGatewayError


class ZarinPalError(PaymentGatewayError):
    """Base class for all ZarinPal errors."""
    def __init__(self, message: str = "An unknown error occurred with ZarinPal."):
        super().__init__(message)
        self.message = message


class ValidationError(ZarinPalError):
    """Raised for general data validation issues."""
    pass


class MerchantIDError(ZarinPalError):
    """Raised when the merchant ID is missing or invalid."""
    def __init__(self):
        super().__init__("Invalid or missing merchant ID.")


class TerminalError(ZarinPalError):
    """Raised when there is an issue with the terminal or merchant permissions."""
    def __init__(self):
        super().__init__("The merchant terminal is blocked, disabled, or does not have access.")


class PaymentError(ZarinPalError):
    """Raised for payment-related errors like insufficient funds or transaction rejection."""
    def __init__(self):
        super().__init__("Transaction could not be completed due to payment issues.")


class SessionError(ZarinPalError):
    """Raised when a payment session is invalid, incomplete, or expired."""
    def __init__(self):
        super().__init__("The payment session is invalid, expired, or was not completed.")


class AuthorityError(ZarinPalError):
    """Raised when an invalid authority code is used or not found."""
    def __init__(self):
        super().__init__("Invalid or unknown authority code.")


class ReverseError(ZarinPalError):
    """Raised for errors occurring during transaction reversal."""
    def __init__(self):
        super().__init__("Unable to reverse the transaction. Please check the transaction status or permissions.")


class AlreadyVerifiedError(ZarinPalError):
    """Raised when trying to verify a transaction that is already verified."""
    def __init__(self):
        super().__init__("This transaction has already been verified.")


class PaymentNotCompletedError(SessionError):
    """Raised when user never completed the payment (canceled, closed page, etc)."""
    def __init__(self):
        super().__init__("The user did not complete the payment session (may have canceled or closed the page).")


ZARINPAL_ERRORS = {
    -9: ValidationError,              # Invalid input
    -10: MerchantIDError,            # Merchant ID not valid
    -11: TerminalError,              # Merchant is blocked
    -12: PaymentError,               # Payment rejected
    -15: TerminalError,              # Terminal does not exist
    -16: TerminalError,              # Terminal is inactive
    -17: TerminalError,              # IP not authorized
    -18: PaymentError,               # Insufficient funds or card error
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
    -50: PaymentNotCompletedError,   # Session not active or abandoned
    -51: SessionError,               # Session expired
    -52: ZarinPalError,              # General internal error
    -53: SessionError,               # Session not found or invalid
    -54: AuthorityError,             # Authority code not valid
    -55: SessionError,               # Session ID is duplicate or reused
    -60: ReverseError,               # Unable to reverse
    -61: ReverseError,               # Already reversed
    -62: ReverseError,               # Reversal not allowed
    -63: ReverseError,               # Reversal time expired
    101: AlreadyVerifiedError,       # Already verified before
}


def get_zarinpal_error(code: int) -> ZarinPalError:
    error_cls = ZARINPAL_ERRORS.get(code, ZarinPalError)
    return error_cls()
