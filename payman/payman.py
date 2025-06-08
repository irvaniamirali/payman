from typing import Any, Callable, Union
from .unified import unified

class Payman:
    def __init__(self, gateway: Any):
        self.gateway = gateway

    def __getattr__(self, item: str) -> Union[Callable[..., Any], Any]:
        attr = getattr(self.gateway, item)
        if callable(attr):
            return unified(attr)
        return attr
