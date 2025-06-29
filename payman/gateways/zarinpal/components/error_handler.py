from typing import Any
from ..errors import get_zarinpal_error


class ErrorHandler:
    def handle(self, response: dict[str, Any]) -> None:
        if not response:
            raise RuntimeError("Empty response from ZarinPal API.")

        if errors := response.get("errors"):
            code = errors["code"]
            raise get_zarinpal_error(code)
