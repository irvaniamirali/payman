class HttpClientError(Exception):
    """Base exception for HTTP client errors."""


class TimeoutError(HttpClientError):
    """Request timed out."""


class HttpStatusError(HttpClientError):
    """HTTP response status code was not successful."""

    def __init__(self, status_code: int, message: str, body: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class InvalidJsonError(HttpClientError):
    """Response JSON could not be decoded."""
