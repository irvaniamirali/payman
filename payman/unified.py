from typing import Callable
from inspect import iscoroutinefunction
import anyio

def unified(func: Callable) -> Callable:
    if not iscoroutinefunction(func):
        return func

    async def dispatch(*args, **kwargs):
        return await func(*args, **kwargs)

    def wrapper(*args, **kwargs):
        try:
            anyio.get_current_task()
            return dispatch(*args, **kwargs)
        except RuntimeError:
            return anyio.run(lambda: dispatch(*args, **kwargs))

    return wrapper
