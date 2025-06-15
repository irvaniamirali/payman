import asyncio
import inspect
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
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                return func(*args, **kwargs)
            else:
                return asyncio.run(func(*args, **kwargs))
        else:
            return func(*args, **kwargs)

    return wrapper


def asyncify(decorator):
    def class_decorator(cls):
        for name, member in inspect.getmembers(cls, inspect.isfunction):
            if inspect.iscoroutinefunction(member):
                setattr(cls, name, decorator(member))
        return cls
    return class_decorator
