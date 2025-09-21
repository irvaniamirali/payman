import asyncio
import time
from json.decoder import JSONDecodeError

import httpx

from payman.core.exceptions.http import (
    HttpClientError,
    HttpStatusError,
    InvalidJsonError,
    TimeoutError
)

from ...interfaces.http import HttpClientProtocol
from .logger import LoggerMixin


class AsyncHttpClient(HttpClientProtocol, LoggerMixin):
    """
    Asynchronous HTTP client with retry, logging, timeout and session management.
    """

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = 10.0,
        slow_request_threshold: float = 3.0,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        log_level: int = 20,
        log_req_body: bool = True,
        log_resp_body: bool = True,
    ):
        LoggerMixin.__init__(self, log_level)
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.timeout = timeout
        self.slow_request_threshold = slow_request_threshold
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.log_req_body = log_req_body
        self.log_resp_body = log_resp_body

        self._client: httpx.AsyncClient | None = None
        self._client_lock = asyncio.Lock()

    async def __aenter__(self) -> "AsyncHttpClient":
        await self._ensure_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def _ensure_client(self) -> httpx.AsyncClient:
        async with self._client_lock:
            if self._client is None:
                self._client = httpx.AsyncClient(timeout=self.timeout)
            return self._client

    async def close(self) -> None:
        async with self._client_lock:
            if self._client is not None:
                await self._client.aclose()
                self._client = None

    async def request(
        self, method: str, endpoint: str, json_data: dict | None = None, **kwargs
    ) -> dict:
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                return await self._send_request(method, endpoint, json_data, **kwargs)
            except HttpClientError as exc:
                last_error = exc
                if attempt < self.max_retries:
                    self.logger.warning(
                        f"Retry {attempt+1}/{self.max_retries} due to {exc}"
                    )
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise
        raise last_error

    async def _send_request(
        self, method: str, endpoint: str, json_data: dict | None = None, **kwargs
    ) -> dict:
        client = await self._ensure_client()

        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            url = endpoint
        else:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"

        headers = kwargs.pop("headers", {})
        kwargs["headers"] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            **headers,
        }

        if self.log_req_body:
            self.log_request(method, url, json_data, debug=True)

        start_time = time.monotonic()
        try:
            response = await client.request(method.upper(), url, json=json_data, **kwargs)
            duration = time.monotonic() - start_time

            if self.log_resp_body:
                self.log_response(method, url, response.text, duration)

            if not response.status_code // 100 == 2:
                raise HttpStatusError(
                    response.status_code,
                    f"HTTP error {response.status_code} from {url}",
                    response.text,
                )

            try:
                return response.json()
            except JSONDecodeError:
                raise InvalidJsonError(f"Invalid JSON from {url}")

        except httpx.TimeoutException as exc:
            raise TimeoutError(str(exc))
        except httpx.RequestError as exc:
            raise HttpClientError(str(exc))
