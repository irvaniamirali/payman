import httpx
import logging
import time
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class API:
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 10,
        slow_threshold: float = 3.0,
        log_request_body: bool = True,
        log_response_body: bool = True,
        max_body_length: int = 500,
        default_headers: Optional[Dict[str, str]] = None,
    ):
        self.base_url = base_url.rstrip('/') if base_url else None
        self.timeout = timeout
        self.slow_threshold = slow_threshold
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.max_body_length = max_body_length
        self.default_headers = default_headers or {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    async def request(self, method: str, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        url = (self.base_url or '') + endpoint
        headers = kwargs.get('headers', {})

        # Merge default headers with custom headers
        headers = {**self.default_headers, **headers}
        kwargs['headers'] = headers

        # Log request
        logger.info(f"[HTTP Request] {method.upper()} {url}")
        if self.log_request_body and kwargs.get('json'):
            body = str(kwargs.get('json'))
            if len(body) > self.max_body_length:
                body = body[:self.max_body_length] + '... [truncated]'
            logger.debug(f"Request Body: {body}")

        start_time = time.monotonic()
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as session:
                response = await session.request(method=method.upper(), url=url, **kwargs)
                response.raise_for_status()
                elapsed = time.monotonic() - start_time

                if elapsed > self.slow_threshold:
                    logger.warning(f"[Slow Request] {method.upper()} {url} took {elapsed:.2f}s")
                else:
                    logger.info(f"[Request Completed] {method.upper()} {url} took {elapsed:.2f}s")

                if self.log_response_body:
                    resp_body = response.text
                    if len(resp_body) > self.max_body_length:
                        resp_body = resp_body[:self.max_body_length] + '... [truncated]'
                    logger.debug(f"Response Body: {resp_body}")

                return response.json()

        except httpx.TimeoutException as e:
            logger.error(f"[Timeout] {method.upper()} {url} - {str(e)}")
            raise APIError(408, "Timeout", str(e))

        except httpx.HTTPStatusError as e:
            logger.error(f"[HTTP Error] {method.upper()} {url} - {e.response.status_code}: {e.response.text}")
            raise APIError(e.response.status_code, "HTTP Error", e.response.text)

        except httpx.RequestError as e:
            logger.error(f"[Request Failed] {method.upper()} {url} - {str(e)}")
            raise APIError(0, "Request failed", str(e))

        except Exception as e:
            logger.exception(f"[Unknown Error] {method.upper()} {url} - {str(e)}")
            raise APIError(0, "Unknown error", str(e))


class APIError(Exception):
    def __init__(self, status_code: int, message: str, detail: Optional[str] = None):
        self.status_code = status_code
        self.message = message
        self.detail = detail
        super().__init__(f"{status_code} {message}: {detail or ''}")
