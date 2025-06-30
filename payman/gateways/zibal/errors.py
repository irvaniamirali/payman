from payman.errors.base import PaymentGatewayError


class ZibalError(PaymentGatewayError):
    """Base class for all Zibal errors."""
    def __init__(self, message: str):
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


class InvalidPercentModeError(ZibalError):
    """Invalid percentMode value (only 0 or 1 allowed)."""
    pass


class InvalidMultiplexingBeneficiariesError(ZibalError):
    """One or more multiplexing beneficiaries are invalid."""
    pass


class InactiveMultiplexingBeneficiaryError(ZibalError):
    """One or more multiplexing beneficiaries are inactive."""
    pass


class MissingSelfBeneficiaryError(ZibalError):
    """'self' beneficiary ID not included in multiplexingInfos."""
    pass


class AmountMismatchInMultiplexingError(ZibalError):
    """Total amount does not match the sum of shares in multiplexingInfos."""
    pass


class InsufficientWalletBalanceForFeesError(ZibalError):
    """Insufficient wallet balance for fee deduction."""
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


ZIBAL_ERRORS = {
    102: MerchantNotFoundError,
    103: MerchantInactiveError,
    104: InvalidMerchantError,
    105: AmountTooLowError,
    106: InvalidCallbackUrlError,
    107: InvalidPercentModeError,
    108: InvalidMultiplexingBeneficiariesError,
    109: InactiveMultiplexingBeneficiaryError,
    110: MissingSelfBeneficiaryError,
    111: AmountMismatchInMultiplexingError,
    112: InsufficientWalletBalanceForFeesError,
    113: AmountExceedsLimitError,
    114: InvalidNationalCodeError,
    201: AlreadyConfirmedError,
    202: PaymentNotSuccessfulError,
    203: InvalidTrackIdError,
}
