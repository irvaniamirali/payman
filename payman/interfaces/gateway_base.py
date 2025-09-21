from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

Request = TypeVar("Request", bound=BaseModel)
Response = TypeVar("Response", bound=BaseModel)


class GatewayInterface(ABC, Generic[Request, Response]):
    """
    Generic interface for payment gateways.

    All gateway classes (e.g., Zibal, ZarinPal) should implement this interface.
    """

    @abstractmethod
    async def initiate_payment(self, request: Request | dict | None = None, **kwargs) -> Response:
        """Initiate a new payment session. Input can be Pydantic model or dict."""

    @abstractmethod
    async def verify_payment(self, request: Request | dict | None = None, **kwargs) -> Response:
        """Verify a payment after user redirection."""

    @abstractmethod
    def get_payment_redirect_url(self, token: str | int) -> str:
        """Return full redirect URL to payment page using the given token."""
