class APIError(Exception):
    def __init__(
        self,
        status_code: int,
        message: str,
        detail: str | None = None,
        headers: dict | None = None,
        body: str | None = None,
    ):
        self.status_code = status_code
        self.message = message
        self.detail = detail
        self.headers = headers
        self.body = body
        super().__init__(self.__str__())

    def __str__(self) -> str:
        base = f"APIError {self.status_code} - {self.message}"
        if self.detail:
            base += f": {self.detail}"
        return base

    def __repr__(self) -> str:
        return (
            f"APIError(status_code={self.status_code!r}, message={self.message!r}, "
            f"detail={self.detail!r}, headers={self.headers!r}, body={self.body!r})"
        )


class InvalidJSONResponseError(APIError):
    def __init__(self, status_code: int, url: str, response_text: str):
        super().__init__(
            status_code,
            "Invalid JSON response from server",
            ""
        )
