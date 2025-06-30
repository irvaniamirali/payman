from typing import Any, Dict
import httpx
import logging
import asyncio
import time
from json.decoder import JSONDecodeError
from .errors import APIError, InvalidJSONResponseError


class API:
    """
    A simple HTTP API client wrapper around httpx.AsyncClient
    with retry, timeout, logging and automatic session management.
    """

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = 10,
        slow_request_threshold: float = 3.0,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        log_level: int = logging.INFO,
        log_request_body: bool = True,
        log_response_body: bool = True,
        max_log_body_length: int = 500,
        default_headers: Dict[str, str] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.timeout = timeout
        self.slow_request_threshold = slow_request_threshold
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.max_log_body_length = max_log_body_length

        self.default_headers = default_headers or {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        self._client: httpx.AsyncClient | None = None
        self._client_lock = asyncio.Lock()

    async def __aenter__(self) -> "API":
        await self._get_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def _get_client(self) -> httpx.AsyncClient:
        """Lazily create and return an httpx.AsyncClient instance."""
        async with self._client_lock:
            if self._client is None:
                self._client = httpx.AsyncClient(timeout=self.timeout)
            return self._client

    async def request(
        self,
        method: str,
        endpoint: str,
        json: Dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Perform an HTTP request with retries, logging and error handling.
        """
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                return await self._perform_request(method, endpoint, json=json, **kwargs)
            except APIError as err:
                last_error = err
                if attempt < self.max_retries:
                    self.logger.warning(
                        f"Retry {attempt + 1}/{self.max_retries} after error: {err}"
                    )
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise
        raise last_error  # type: ignore

    async def _perform_request(
            self,
            method: str,
            endpoint: str,
            json: Dict[str, Any] | None = None,
            **kwargs: Any,
    ) -> Dict[str, Any]:
        client = await self._get_client()
        url = f"{self.base_url}{endpoint}"

        headers = kwargs.pop("headers", {})
        headers = {**self.default_headers, **headers}
        kwargs["headers"] = headers

        if self.logger.isEnabledFor(logging.INFO):
            self.logger.info(f"HTTP {method.upper()} {url}")

        if self.log_request_body and json and self.logger.isEnabledFor(logging.DEBUG):
            body_preview = str(json)
            if len(body_preview) > self.max_log_body_length:
                body_preview = body_preview[: self.max_log_body_length] + "... [truncated]"
            self.logger.debug(f"Request Body: {body_preview}")

        start_time = time.monotonic()

        try:
            response = await client.request(
                method=method.upper(),
                url=url,
                json=json,
                **kwargs,
            )
            duration = time.monotonic() - start_time

            if duration > self.slow_request_threshold:
                self.logger.warning(f"Slow request: {method.upper()} {url} took {duration:.2f}s")
            else:
                self.logger.info(f"Request completed: {method.upper()} {url} took {duration:.2f}s")

            if self.log_response_body and self.logger.isEnabledFor(logging.DEBUG):
                response_text = response.text
                if len(response_text) > self.max_log_body_length:
                    response_text = response_text[: self.max_log_body_length] + "... [truncated]"
                self.logger.debug(f"Response Body: {response_text}")

            try:
                return response.json()
            except JSONDecodeError:
                self.logger.error(f"Invalid JSON from {url}: {response.text[:200]!r}")
                raise InvalidJSONResponseError(response.status_code, url, response.text)

        except InvalidJSONResponseError:
            raise

        except httpx.TimeoutException as exc:
            self.logger.error(f"Timeout during {method.upper()} {url}: {exc}")
            raise APIError(408, "Timeout", str(exc))

        except httpx.HTTPStatusError as exc:
            self.logger.error(f"HTTP error {exc.response.status_code} during {method.upper()} {url}: {exc.response.text}")
            raise APIError(
                exc.response.status_code,
                "HTTP Error",
                exc.response.text,
                headers=exc.response.headers,
                body=exc.response.text,
            )

        except httpx.RequestError as exc:
            self.logger.error(f"Request failed during {method.upper()} {url}: {exc}")
            raise APIError(0, "Request failed", str(exc))

        except Exception as exc:
            self.logger.exception(f"Unexpected error during {method.upper()} {url}: {exc}")
            raise APIError(0, "Unknown error", str(exc))

    async def close(self) -> None:
        """Close the underlying HTTP client session."""
        if self._client:
            await self._client.aclose()
            self._client = None
