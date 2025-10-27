import concurrent.futures
from typing import Callable

_executor = concurrent.futures.ThreadPoolExecutor()

def make_async(func:Callable) -> Callable:
    def wrapper(*args, **kwargs) -> None:
        _executor.submit(func, *args, **kwargs)
    return wrapper