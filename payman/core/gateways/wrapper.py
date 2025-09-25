from typing import TYPE_CHECKING, Literal, overload

from payman.interfaces.gateway_base import GatewayInterface

from .register_gateway import get_gateway_instance

if TYPE_CHECKING:
    from zarinpal import ZarinPal
    from zibal import Zibal


class Payman:
    """
    Factory-like class for creating payment gateway instances.

    This class acts as a type-safe factory. Depending on the `name` argument, it returns
    an instance of the corresponding payment gateway (e.g., `Zibal`, `ZarinPal`)
    implementing `GatewayInterface`.

    Features:
        - IDE autocomplete works with typed return thanks to overloads.
        - Typed return ensures proper type hints for gateway-specific methods.
        - Supports any registered gateway via `get_gateway_instance`.

    Usage:
        >>> zibal = Payman("zibal", merchant_id="xyz")
        >>> zarinpal = Payman("zarinpal", merchant_id="abc")

    Overloads:
        - Payman("zibal", merchant_id=..., **kwargs) -> Zibal
        - Payman("zarinpal", merchant_id=..., **kwargs) -> ZarinPal
        - Payman(name: str, **kwargs) -> GatewayInterface (for other gateways)

    Args:
        name (str): The gateway name (case-insensitive).
        **kwargs: Arguments passed to the gateway constructor.

    Returns:
        GatewayInterface: An instance of the requested gateway.

    Raises:
        ValueError: If the requested gateway is not registered.
        TypeError: If the gateway constructor fails.
    """

    @overload
    def __new__(cls, name: Literal["zarinpal"], *, merchant_id: str, **kwargs) -> "ZarinPal": ...
    @overload
    def __new__(cls, name: Literal["zibal"], *, merchant_id: str, **kwargs) -> "Zibal": ...
    @overload
    def __new__(cls, name: str, **kwargs) -> GatewayInterface: ...

    def __new__(cls, name: str, **kwargs) -> GatewayInterface:
        return get_gateway_instance(name, **kwargs)
