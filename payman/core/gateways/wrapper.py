from typing import TYPE_CHECKING, Literal, overload

from payman.interfaces.gateway_base import GatewayInterface

from .register_gateway import get_gateway_instance

if TYPE_CHECKING:
    from zarinpal import ZarinPal
    from zibal import Zibal


@overload
def Payman(name: Literal["zarinpal"], *, merchant_id: str, **kwargs) -> "ZarinPal": ...
@overload
def Payman(name: Literal["zibal"], *, merchant_id: str, **kwargs) -> "Zibal": ...
@overload
def Payman(name: str, **kwargs) -> GatewayInterface: ...


def Payman(name: str, **kwargs) -> GatewayInterface:
    """
    Factory function to create payment gateway instances.
    """
    return get_gateway_instance(name, **kwargs)
