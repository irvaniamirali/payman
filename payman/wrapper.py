from typing import Literal, overload
from .gateways import GatewayInterface, create_gateway
from .gateways import ZarinPal, Zibal


@overload
def payman(name: Literal["zarinpal"], *, merchant_id: str, **kwargs) -> ZarinPal: ...

@overload
def payman(name: Literal["zibal"], *, merchant_id: str, **kwargs) -> Zibal: ...

@overload
def payman(name: str, **kwargs) -> GatewayInterface: ...


def payman(name: str, **kwargs) -> GatewayInterface:
    """
    Factory function to create payment gateway instances.

    Args:
        name: Name of the gateway, e.g. "zarinpal" or "zibal"
        kwargs: Arguments to pass to the gateway constructor,
                e.g. merchant_id and others.

    Usage:
    >>> from payman import Payman
    >>> pay = Payman("zibal", merchant_id="...")
    >>> res = await pay.payment(
    ...     amount=10000,
    ...     callback_url="https://yourdomain.com/callback",
    ...     description="..."
    ... )
    >>> print(res.success)

    Returns:
        Instance of a class implementing GatewayInterface.

    Raises:
        ValueError: If the gateway name is unknown.
    """
    return create_gateway(name, **kwargs)
