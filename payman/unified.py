import inspect
from asyncio import run, get_running_loop
from functools import wraps

def flexcall(func):
    """
    Allows async functions to be called transparently from sync or async contexts,
    avoiding asyncio.run inside a running loop.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if inspect.iscoroutinefunction(func):
            try:
                loop = get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                return func(*args, **kwargs)
            else:
                return run(func(*args, **kwargs))
        else:
            return func(*args, **kwargs)

    return wrapper


class Asyncifiable:
    """
    Base class that automatically wraps coroutine methods
    with `flexcall` so they can be called both asynchronously and synchronously.

    Any subclass inheriting from this will automatically get dual-mode (sync + async)
    support for its async methods.
    """
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        for attr_name, attr in cls.__dict__.items():
            if inspect.iscoroutinefunction(attr) and not attr_name.startswith("_"):
                setattr(cls, attr_name, flexcall(attr))
