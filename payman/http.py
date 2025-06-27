from typing import Any, Dict
import httpx
import logging
import asyncio
import time


class API:
    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = 10,
        slow_threshold: float = 3.0,
        retry_count: int = 0,
        retry_delay: float = 1.0,
        log_level: int = logging.INFO,
        log_request_body: bool = True,
        log_response_body: bool = True,
        max_body_length: int = 500,
        default_headers: Dict[str, str] | None = None,
    ):
        self.base_url = base_url.rstrip("/") if base_url else None
        self.timeout = timeout
        self.slow_threshold = slow_threshold
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.max_body_length = max_body_length
        self.default_headers = default_headers or {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def request(self, method: str, endpoint: str, json: dict = None, **kwargs):
        last_exc = None
        for attempt in range(self.retry_count + 1):
            try:
                return await self._request(method, endpoint, json, **kwargs)
            except APIError as e:
                last_exc = e
                if attempt < self.retry_count:
                    self.logger.warning(
                        f"Retrying ({attempt + 1}/{self.retry_count}) after error: {e}"
                    )
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise
        raise last_exc

    async def _request(self, method: str, endpoint: str, json: dict = None, **kwargs: Any) -> Dict[str, Any]:
        url = (self.base_url or "") + endpoint
        headers = kwargs.pop("headers", {})
        headers = {**self.default_headers, **headers}
        kwargs["headers"] = headers
        if self.logger.isEnabledFor(logging.INFO):
            self.logger.info(f"[HTTP Request] {method.upper()} {url}")

        if self.log_request_body and json and self.logger.isEnabledFor(logging.DEBUG):
            body = str(json)
            if len(body) > self.max_body_length:
                body = body[: self.max_body_length] + "... [truncated]"
            self.logger.debug(f"Request Body: {body}")

        start_time = time.monotonic()
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as session:
                response = await session.request(
                    method=method.upper(), url=url, json=json, **kwargs
                )
                print(response)
                elapsed = time.monotonic() - start_time

                if elapsed > self.slow_threshold:
                    self.logger.warning(
                        f"[Slow Request] {method.upper()} {url} took {elapsed:.2f}s"
                    )
                else:
                    self.logger.info(
                        f"[Request Completed] {method.upper()} {url} took {elapsed:.2f}s"
                    )

                if self.log_response_body and self.logger.isEnabledFor(logging.DEBUG):
                    resp_body = response.text
                    if len(resp_body) > self.max_body_length:
                        resp_body = (
                            resp_body[: self.max_body_length] + "... [truncated]"
                        )
                    self.logger.debug(f"Response Body: {resp_body}")

                return response.json()

        except httpx.TimeoutException as e:
            self.logger.error(f"[Timeout] {method.upper()} {url} - {str(e)}")
            raise APIError(408, "Timeout", str(e))

        except httpx.HTTPStatusError as e:
            self.logger.error(
                f"[HTTP Error] {method.upper()} {url} - {e.response.status_code}: {e.response.text}"
            )
            raise APIError(
                e.response.status_code,
                "HTTP Error",
                e.response.text,
                headers=e.response.headers,
                body=e.response.text,
            )

        except httpx.RequestError as e:
            self.logger.error(f"[Request Failed] {method.upper()} {url} - {str(e)}")
            raise APIError(0, "Request failed", str(e))

        except Exception as e:
            self.logger.exception(f"[Unknown Error] {method.upper()} {url} - {str(e)}")
            raise APIError(0, "Unknown error", str(e))


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
