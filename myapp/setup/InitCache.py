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

    prefix = f"{func.__module__}.{func.__name__}"
    print(prefix + "|".join(data) )
    return f"{prefix}:" + "|".join(data)


def init_cache(app: Flask) -> Cache:
    cache.init_app(app)

    return cache
