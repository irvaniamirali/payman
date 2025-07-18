from typing import Type, cast

from .interface import GatewayInterface
from .zarinpal import ZarinPal
from .zibal import Zibal

# Gateway registry mapping string names to gateway classes
GATEWAY_REGISTRY: dict[str, Type[GatewayInterface]] = {
    "zibal": Zibal,
    "zarinpal": ZarinPal,
}


def register_gateway(name: str, cls: Type[GatewayInterface]) -> None:
    """
    Register a new payment gateway class.

    Args:
        name: Unique name for the gateway (e.g., "payping").
        cls: Class implementing the GatewayInterface.
    """
    GATEWAY_REGISTRY[name.lower()] = cls


def create_gateway(name: str, **kwargs) -> GatewayInterface:
    """
    Create an instance of the specified payment gateway.

    Args:
        name: The name of the gateway (e.g., "zibal", "zarinpal").
        **kwargs: Keyword arguments to pass to the gateway constructor.

    Returns:
        An instance of a class implementing GatewayInterface.

    Raises:
        ValueError: If the gateway name is not registered.
    """
    gateway_cls = GATEWAY_REGISTRY.get(name.lower())
    if not gateway_cls:
        available = ", ".join(GATEWAY_REGISTRY.keys())
        raise ValueError(f"Gateway '{name}' not supported. Available: [{available}]")
    return cast(GatewayInterface, gateway_cls(**kwargs))
