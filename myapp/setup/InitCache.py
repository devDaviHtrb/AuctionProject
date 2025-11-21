from flask import Flask
from flask_caching import Cache
from typing import Callable

cache = Cache()
redis_conn = None

from typing import Callable

def cache_key(func: Callable, *args, **kwargs) -> str:
    data = []
    for key, value in sorted(kwargs.items()):
        if hasattr(value, "__mapper__"):
            pk_cols = value.__mapper__.primary_key
            pk_values = [getattr(value, col.name) for col in pk_cols]
            data.append(f"{key}={ '-'.join(str(v) for v in pk_values) }")
        else:
            data.append(f"{key}={value}")

    return prefix + ":" + "|".join(parts)


def cached(timeout: int = 300) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            key: str = build_cache_key(func, args, kwargs)
            cached_value: Optional[Any] = cache.get(key)

            if cached_value is not None:
                return cached_value

            result: Any = func(*args, **kwargs)
            #cache.set(key, result, timeout=timeout)
            print(key, flush=True)
            return result

        return wrapper
    return decorator
    prefix = f"{func.__module__}.{func.__name__}"
    print(prefix + "|".join(data) )
    return f"{prefix}:" + "|".join(data)


def init_cache(app: Flask) -> Cache:
    cache.init_app(app)

    return cache
