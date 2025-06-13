from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import TypeVar, Generic

Req = TypeVar("Req", bound=BaseModel)
Res = TypeVar("Res", bound=BaseModel)

class PaymentRequestor(Generic[Req, Res], ABC):
    @abstractmethod
    async def request_payment(self, request: Req) -> Res: ...

class PaymentVerifier(Generic[Req, Res], ABC):
    @abstractmethod
    async def verify(self, request: Req) -> Res: ...

class PaymentURLGenerator(ABC):
    @abstractmethod
    async def payment_url_generator(self, authority: str) -> str: ...

class PaymentInquirer(Generic[Req, Res]):
    @abstractmethod
    async def inquiry(self, request: Req) -> Res: ...

class CallbackVerifier(Generic[Req, Res]):
    @abstractmethod
    async def callback_verify(self, callback: Req) -> Res: ...

class LazyPaymentRequestor(Generic[Req, Res], ABC):
    @abstractmethod
    async def request_lazy_payment(self, request: Req) -> Res: ...

class LazyCallbackVerifier(Generic[Req, Res], ABC):
    @abstractmethod
    async def verify_lazy_callback(self, callback: Req) -> Res: ...
