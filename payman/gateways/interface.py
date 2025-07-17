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
    async def payment(self, request: Request | dict | None = None, **kwargs) -> Response:
        """
        Initiate a new payment session.

        Args:
            request (Request | dict): Payment input parameters.
                Can be passed as a Pydantic model, dictionary, or directly via keyword arguments.

        Returns:
            Response: Response including authority/track_id and status.

        Example:
        >>> from payman import Payman
        >>> pay = Payman("zibal", merchant_id="...")
        >>> res = await pay.payment(
        ...     amount=10000,
        ...     callback_url="https://yourdomain.com/callback",
        ...     mobile="09123456789",
        ... )
        >>> print("Redirect the user to:", res.payment_url)
        """
        raise NotImplementedError

    @abstractmethod
    async def verify(self, request: Request | dict | None = None, **kwargs) -> Response:
        """
        Verify a payment after the user is redirected back.

        Args:
            request (VerifyRequest | dict, optional): Verification input.
                Can be passed as a Pydantic model,
                dictionary, or directly via keyword arguments.

        Returns:
            Response: Response with transaction status and details.

        Example:
            >>> from payman import Payman
            >>> pay = Payman("zibal", merchant_id="...")
            >>> res = await pay.verify(
            ...     track_id="A1B2C3D4",
            ... )
            >>> if res.success:
            ...     print("Payment was successful.")
            ... else:
            ...     print("Payment failed or was not verified. error message: ", res.message)
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
    @property
    @abstractmethod
    def is_success(self) -> bool:
        """
        Indicates whether the callback represents a successful payment.
        """
        pass
