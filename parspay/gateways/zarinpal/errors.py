class ZarinPalVerificationError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Verification failed with code {code}: {message}")
