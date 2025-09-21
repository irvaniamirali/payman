from typing import Any


class HttpClientProtocol:
    """Protocol for any HTTP client."""

    async def request(
        self,
        method: str,
        endpoint: str,
        json_data: dict[str, Any] | None = None,
        **kwargs: Any
    ) -> dict[str, Any]: ...
