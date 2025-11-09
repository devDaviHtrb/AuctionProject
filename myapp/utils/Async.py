import concurrent.futures
from typing import Callable

_executor = concurrent.futures.ThreadPoolExecutor(max_workers=6)

def make_async(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        return _executor.submit(func, *args, **kwargs)
    return wrapper
