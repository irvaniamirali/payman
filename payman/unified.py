import inspect
import asyncio
from functools import wraps


def is_async() -> bool:
    """
    Check if there's an active asyncio event loop.
    Returns True if running inside an async context.
    """
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False


def sync_async_bridge(func):
    """
    Decorator that makes a coroutine function callable in both sync and async contexts.

    - If called in an async context, it returns the coroutine.
    - If called in a sync context, it runs the coroutine using `asyncio.run()`.

    Useful for building user-friendly APIs that can be used in both environments.
    """
    if not inspect.iscoroutinefunction(func):
        raise TypeError("sync_async_bridge can only be used with async functions")

    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_async():
            return func(*args, **kwargs)
        return asyncio.run(func(*args, **kwargs))

    return wrapper


class AsyncCapable:
    """
    Mixin that makes all async public methods of a class usable synchronously via sync_async_bridge.

    This avoids the need for users to manually handle event loops.
    """
    def __init_subclass__(cls):
        for name in dir(cls):
            if name.startswith("_") or name in {"__aenter__", "__aexit__"}:
                continue

            attr = getattr(cls, name)
            if inspect.isfunction(attr) and asyncio.iscoroutinefunction(attr):
                setattr(cls, name, sync_async_bridge(attr))
