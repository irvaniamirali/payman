import logging


class LoggerMixin:
    def __init__(self, log_level: int = logging.INFO, max_body_length: int = 500):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)
        self.max_body_length = max_body_length

    def log_request(
        self, method: str, url: str, json_data: dict | None = None, debug: bool = True
    ):
        self.logger.info(f"HTTP {method.upper()} {url}")
        if json_data and debug and self.logger.isEnabledFor(logging.DEBUG):
            body = str(json_data)
            if len(body) > self.max_body_length:
                body = f"{body[:self.max_body_length]}... [truncated]"
            self.logger.debug(f"Request Body: {body}")

    def log_response(self, method: str, url: str, response_text: str, duration: float):
        if duration > 3.0:  # slow request threshold
            self.logger.warning(
                f"Slow request: {method.upper()} {url} took {duration:.2f}s"
            )
        else:
            self.logger.info(
                f"Request completed: {method.upper()} {url} took {duration:.2f}s"
            )

        if self.logger.isEnabledFor(logging.DEBUG):
            body = response_text
            if len(body) > self.max_body_length:
                body = f"{body[:self.max_body_length]}... [truncated]"
            self.logger.debug(f"Response Body: {body}")
