from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import TypeVar, Generic

Req = TypeVar("Req", bound=BaseModel)
Res = TypeVar("Res", bound=BaseModel)

class GatewayInterface(Generic[Req, Res], ABC):
    """Base interface for all payment gateways"""

    @abstractmethod
    async def request_payment(self, request: Req) -> Res:
        ...

    @abstractmethod
    async def verify(self, request: Req) -> Res:
        ...

    @abstractmethod
    def payment_url_generator(self, authority: str) -> str:
        ...

    @abstractmethod
    async def inquiry(self, request: Req) -> Res:
        ...

    @abstractmethod
    async def callback_verify(self, callback: Req) -> Res:
        ...

    @abstractmethod
    async def request_lazy_payment(self, request: Req) -> Res:
        ...

    @abstractmethod
    async def verify_lazy_callback(self, callback: Req) -> Res:
        ...


class BaseGateway(GatewayInterface):
    async def request_payment(self, request):
        raise NotImplementedError(f"{self.__class__.__name__} does not support `request_payment()`.")

    async def verify(self, request):
        raise NotImplementedError(f"{self.__class__.__name__} does not support `verify_payment()`.")

    def payment_url_generator(self, authority: str) -> str:
        raise NotImplementedError(f"{self.__class__.__name__} does not support `payment_url_generator()`.")

    async def request_lazy_payment(self, request):
        raise NotImplementedError(f"{self.__class__.__name__} does not support `request_lazy_payment()`.")

    async def verify_lazy_callback(self, callback):
        raise NotImplementedError(f"{self.__class__.__name__} does not support `verify_lazy_callback()`.")

    async def inquiry(self, request):
        raise NotImplementedError(f"{self.__class__.__name__} does not support `inquiry()`.")

    async def callback_verify(self, callback):
        raise NotImplementedError(f"{self.__class__.__name__} does not support `callback_verify()`.")
