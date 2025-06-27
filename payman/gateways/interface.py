from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel

Request = TypeVar("Request", bound=BaseModel)
Response = TypeVar("Response", bound=BaseModel)
Callback = TypeVar("Callback", bound=BaseModel)


class GatewayInterface(ABC, Generic[Request, Response, Callback]):
    """
    Generic interface for implementing a payment gateway.

    All payment gateway classes (e.g. Zibal, ZarinPal) should inherit from this interface
    and implement the required methods. This promotes consistency and clean architecture.

    - `Request`: Input model for initiating or verifying a transaction.
    - `Response`: Output model (response).
    - `Callback`: Callback model used for verification after user returns from payment gateway.
    """

    @abstractmethod
    async def payment(self, request: Request) -> Response:
        """
        Initiate a new payment session.

        Args:
            request (Request): PaymentRequest model instance.

        Returns:
            Response: PaymentResponse including authority/track_id and status.
        """
        raise NotImplementedError

    @abstractmethod
    async def verify(self, request: Request) -> Response:
        """
        Verify a payment after the user is redirected back.

        Args:
            request (Request): VerifyRequest model containing track_id or token.

        Returns:
            Response: VerifyResponse with transaction status and details.
        """
        raise NotImplementedError

    @abstractmethod
    def get_payment_redirect_url(self, token: str | int) -> str:
        """
        Construct the redirect URL to the payment gateway page.

        Args:
            token (str | int): Track ID or authority depending on the gateway.

        Returns:
            str: Full redirect URL.
        """
        raise NotImplementedError


class CallbackBase(ABC):
    @abstractmethod
    def is_successful(self) -> bool:
        """
        Indicates whether the callback represents a successful payment.
        """
        pass
