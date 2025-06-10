
class ZarinPalVerificationError(Exception):
    def __init__(self, code: int, message: str = ""):
        self.code = code
        self.message = message
        super().__init__(f"ZarinPal error {code}: {message}")


ZARINPAL_ERROR_MESSAGES = {
    -9: "Validation error",
    -10: "Terminal is not valid. Check merchant_id or IP address.",
    -11: "Terminal is not active. Contact support.",
    -12: "Too many attempts. Please try again later.",
    -15: "Terminal is suspended. Contact support.",
    -16: "User level is below silver. Contact support.",
    -17: "User is restricted at Blue level. Contact support.",
    -18: "Referrer address mismatch. Domain not allowed.",
    -19: "Transactions are disabled for this terminal.",
    -30: "Terminal not allowed to use floating wages.",
    -31: "No default bank account. Add one in panel.",
    -32: "Wage amount exceeds total transaction amount.",
    -33: "Invalid wage percentage.",
    -34: "Fixed wage exceeds total transaction amount.",
    -35: "Too many wage recipients.",
    -36: "Minimum wage amount is 10,000 Rials.",
    -37: "One or more IBANs are inactive.",
    -38: "IBAN not defined properly in Shaparak.",
    -39: "General wage error. Contact support.",
    -40: "Invalid extra params. `expire_in` is not valid.",
    -41: "Maximum amount is 100,000,000 tomans.",
    -50: "Amount mismatch during verification.",
    -51: "Unsuccessful payment session.",
    -52: "Unexpected error. Contact support.",
    -53: "Session does not belong to this merchant.",
    -54: "Invalid authority.",
    -55: "Manual payment request not found.",
    -60: "Cannot reverse session with bank.",
    -61: "Transaction not successful or already reversed.",
    -62: "Terminal IP restriction not active.",
    -63: "Reverse timeout expired (30 minutes).",
}
