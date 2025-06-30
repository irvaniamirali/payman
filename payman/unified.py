import asyncio
import inspect
import threading
import functools


def convert_async_gen_to_sync(async_gen, loop, is_main_thread):
    async def anext(agen):
        try:
            return await agen.__anext__(), False
        except StopAsyncIteration:
            return None, True

    while True:
        if is_main_thread:
            item, done = loop.run_until_complete(anext(async_gen))
        else:
            item, done = asyncio.run_coroutine_threadsafe(anext(async_gen), loop).result()

        if done:
            break
        yield item


def make_async_method_sync_compatible(obj, method_name):
    async_method = getattr(obj, method_name)
    main_event_loop = asyncio.get_event_loop()

    @functools.wraps(async_method)
    def sync_wrapper(*args, **kwargs):
        coro_or_asyncgen = async_method(*args, **kwargs)

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        is_async_gen = inspect.isasyncgen(coro_or_asyncgen)
        is_coro = inspect.iscoroutine(coro_or_asyncgen)

        if threading.current_thread() is threading.main_thread() or not main_event_loop.is_running():
            if loop.is_running():
                # If loop is running, return coroutine as-is for async usage
                return coro_or_asyncgen
            elif is_coro:
                # Run coroutine to completion synchronously
                return loop.run_until_complete(coro_or_asyncgen)
            elif is_async_gen:
                # Convert async generator to sync generator
                return convert_async_gen_to_sync(coro_or_asyncgen, loop, True)
        else:
            # Running in a non-main thread
            if is_coro:
                # Submit coroutine to main loop and wait for result
                return asyncio.run_coroutine_threadsafe(coro_or_asyncgen, main_event_loop).result()
            elif is_async_gen:
                # Convert async generator to sync generator using main loop
                return convert_async_gen_to_sync(coro_or_asyncgen, main_event_loop, False)

    setattr(obj, method_name, sync_wrapper)


def wrap_async_methods_as_sync(obj):
    for attr_name in dir(obj):
        if attr_name.startswith("_"):
            continue
        attr = getattr(obj, attr_name)
        if inspect.iscoroutinefunction(attr) or inspect.isasyncgenfunction(attr):
            make_async_method_sync_compatible(obj, attr_name)


class AsyncSyncMixin:
    """
    Mixin class that automatically wraps async methods
    to support synchronous calling as well.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        wrap_async_methods_as_sync(cls)
