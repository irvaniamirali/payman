from importlib import import_module
from typing import Type, cast

from payman.interfaces.gateway_base import GatewayInterface

# Gateway registry: maps gateway name to its class or import path
_GATEWAY_REGISTRY: dict[str, Type[GatewayInterface] | str] = {
    "zibal": "zibal.Zibal",
}


def register_gateway(name: str, import_path: str) -> None:
    """
    Dynamically register a new payment gateway.

    Args:
        name: Unique gateway identifier (e.g., "zibal").
        import_path: Dotted path to the gateway class
                     (e.g., "zibal.gateway.Zibal").
    """

    _GATEWAY_REGISTRY[name.lower()] = import_path


def _load_class(import_path: str) -> Type[GatewayInterface]:
    """
    Import a class dynamically from a dotted path.

    Args:
        import_path: e.g., "zibal.Zibal"

    Returns:
        Class type implementing GatewayInterface.

    Raises:
        ImportError: if module cannot be imported
        AttributeError: if class not found in module
    """

    module_name, class_name = import_path.rsplit(".", 1)
    module = import_module(module_name)
    try:
        cls = getattr(module, class_name)
    except AttributeError as exc:
        raise ImportError(f"Class '{class_name}' not found in module '{module_name}'") from exc
    return cast(Type[GatewayInterface], cls)


def get_gateway_instance(name: str, **kwargs) -> GatewayInterface:
    """
    Return an instance of the requested payment gateway.

    Args:
        name: Gateway name (case-insensitive)
        **kwargs: Keyword arguments for the gateway constructor

    Returns:
        GatewayInterface instance

    Raises:
        ValueError: if gateway is not registered
        ImportError: if gateway module/class is missing
    """

    key = name.lower()
    registry_entry = _GATEWAY_REGISTRY.get(key)
    if not registry_entry:
        available = ", ".join(_GATEWAY_REGISTRY.keys())
        raise ValueError(f"Gateway '{name}' not supported. Available: [{available}]")

    if isinstance(registry_entry, str):
        cls = _load_class(registry_entry)
        # cache class to avoid re-import
        _GATEWAY_REGISTRY[key] = cls
    else:
        cls = registry_entry

    try:
        return cls(**kwargs)
    except TypeError as exc:
        raise TypeError(f"Failed to instantiate '{name}' gateway: {exc}") from exc
