import concurrent.futures
from typing import Callable, Tuple, Any, List, Dict, Optional
from flask import current_app

_executor = concurrent.futures.ThreadPoolExecutor(max_workers=6)


def make_async(func: Callable[..., Any]) -> Callable:
    def wrapper(*args, **kwargs):
        return _executor.submit(func, *args, **kwargs)
    return wrapper


def run_async_functions(
    funcs: List[Tuple[Callable[..., Any], Tuple[Any, ...], Dict[str, Any]]]
) -> Tuple[Any, ...]:
    
    futures = []

    app: Optional[Any] = None
    try:
        app = current_app._get_current_object()
    except Exception:
        pass  

    for func, args, kwargs in funcs:
        def wrapped_func(f=func, a=args, k=kwargs):
            if app is not None:
                with app.app_context():
                    return f(*a, **k)
            else:
                return f(*a, **k)

        futures.append(_executor.submit(wrapped_func))

    results: List[Any] = []
    for f in futures:
        try:
            results.append(f.result())
        except Exception as e:
            results.append(e)

    return tuple(results)
