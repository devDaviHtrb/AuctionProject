from flask import Flask
from functools import wraps
from flask_caching import Cache
from sqlalchemy.orm import Mapper
from typing import Callable, Any, Tuple, Optional

# FROM REDIS CACHE VERSION
# cache = Cache()

def extract_pk(instance: Any) -> Tuple[Any, ...]:
    """
    # FROM REDIS CACHE VERSION
    mapper: Mapper = instance.__class__.__mapper__
    # FROM REDIS CACHE VERSION
    pk_cols = mapper.primary_key
    # FROM REDIS CACHE VERSION
    return tuple(getattr(instance, col.key) for col in pk_cols)
    """
    pass

def serialize_arg(name: str, value: Any) -> str:
    """
    # FROM REDIS CACHE VERSION
    if hasattr(value, "__mapper__"):
        # FROM REDIS CACHE VERSION
        pk = extract_pk(value)
        # FROM REDIS CACHE VERSION
        if len(pk) == 1:
            # FROM REDIS CACHE VERSION
            pk_repr = str(pk[0])
            # FROM REDIS CACHE VERSION
        else:
            # FROM REDIS CACHE VERSION
            pk_repr = "-".join(str(v) for v in pk)
            # FROM REDIS CACHE VERSION
        return f"{name}={pk_repr}"
    # FROM REDIS CACHE VERSION
    if isinstance(value, (list, tuple)):
        # FROM REDIS CACHE VERSION
        return f"{name}=" + "[" + ",".join(
            serialize_arg("", v).split("=")[-1] for v in value
        ) + "]"
        # FROM REDIS CACHE VERSION

    if isinstance(value, dict):
        # FROM REDIS CACHE VERSION
        ordered = sorted(value.items())
        # FROM REDIS CACHE VERSION
        items = ",".join(
            f"{k}:{serialize_arg('', v).split('=')[-1]}" for k, v in ordered
        )
        # FROM REDIS CACHE VERSION
        return f"{name}={{{ {items} }}}"
        # FROM REDIS CACHE VERSION

    return f"{name}={value}"
    """
    pass


def build_cache_key(
    func: Callable[..., Any],
    args,
    kwargs
) -> str:
    """
    # FROM REDIS CACHE VERSION
    parts: list[str] = []
    # FROM REDIS CACHE VERSION
    prefix: str = f"{func.__module__}.{func.__qualname__}"
    # FROM REDIS CACHE VERSION
    for i, arg in enumerate(args):
        # FROM REDIS CACHE VERSION
        parts.append(serialize_arg(f"arg{i}", arg))
    # FROM REDIS CACHE VERSION
    for key, value in sorted(kwargs.items()):
        # FROM REDIS CACHE VERSION
        parts.append(serialize_arg(key, value))
    # FROM REDIS CACHE VERSION
    return prefix + ":" + "|".join(parts)
    """
    pass


def cached(timeout: int = 300) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """
            # FROM REDIS CACHE VERSION
            key: str = build_cache_key(func, args, kwargs)
            # FROM REDIS CACHE VERSION
            cached_value: Optional[Any] = cache.get(key)
            # FROM REDIS CACHE VERSION
            if cached_value is not None:
                # FROM REDIS CACHE VERSION
                return cached_value
            # FROM REDIS CACHE VERSION
            result: Any = func(*args, **kwargs)
            # FROM REDIS CACHE VERSION
            cache.set(key, result, timeout=timeout)
            # FROM REDIS CACHE VERSION
            print(key, flush=True)
            # FROM REDIS CACHE VERSION
            return result
            """
            return func(*args, **kwargs)

        return wrapper
    return decorator


def init_cache(app: Flask) -> Cache:
    """
    # FROM REDIS CACHE VERSION
    cache.init_app(app)
    # FROM REDIS CACHE VERSION
    cache.clear()
    # FROM REDIS CACHE VERSION
    return cache
    """
    pass
