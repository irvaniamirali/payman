from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import TypeVar, Generic

Request = TypeVar("Request", bound=BaseModel)
Response = TypeVar("Response", bound=BaseModel)

class BaseGateway(Generic[Request, Response], ABC):
    """Base interface for all payment gateways"""

    @abstractmethod
    async def payment(self, request: Request) -> Response:
        ...

    @abstractmethod
    async def verify(self, request: Request) -> Response:
        ...

    @abstractmethod
    def payment_url_generator(self, authority: str) -> str:
        ...

    @abstractmethod
    async def inquiry(self, request: Request) -> Response:
        ...

    @abstractmethod
    async def callback_verify(self, callback: Request) -> Response:
        ...

    @abstractmethod
    async def lazy_payment(self, request: Request) -> Response:
        ...

    @abstractmethod
    async def verify_lazy_callback(self, callback: Request) -> Response:
        ...


class GatewayInterface(BaseGateway):

    async def payment(self, request):
        raise NotImplementedError(f"{self.__class__.__name__} does not support `payment()`.")

    async def verify(self, request):
        raise NotImplementedError(f"{self.__class__.__name__} does not support `payment()`.")

    def payment_url_generator(self, authority: str) -> str:
        raise NotImplementedError(f"{self.__class__.__name__} does not support `payment_url_generator()`.")

    async def lazy_payment(self, request):
        raise NotImplementedError(f"{self.__class__.__name__} does not support `lazy_payment()`.")

    async def verify_lazy_callback(self, callback):
        raise NotImplementedError(f"{self.__class__.__name__} does not support `verify_lazy_callback()`.")

    async def inquiry(self, request):
        raise NotImplementedError(f"{self.__class__.__name__} does not support `inquiry()`.")

    async def callback_verify(self, callback):
        raise NotImplementedError(f"{self.__class__.__name__} does not support `callback_verify()`.")
