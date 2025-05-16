from typing import Callable
from inspect import iscoroutinefunction
import anyio

def unified(func: Callable) -> Callable:
    async def dispatch(*args, **kwargs):
        if iscoroutinefunction(func):
            return await func(*args, **kwargs)
        return func(*args, **kwargs)

    def wrapper(*args, **kwargs):
        try:
            anyio.get_current_task()
            return dispatch(*args, **kwargs)
        except RuntimeError:
            return anyio.run(lambda: dispatch(*args, **kwargs))

    return wrapper
