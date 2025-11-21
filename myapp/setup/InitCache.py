from flask import Flask
from functools import wraps
from flask_caching import Cache
from sqlalchemy.orm import Mapper
from typing import Callable, Any, Tuple, Optional

cache = Cache()

def extract_pk(instance: Any) -> Tuple[Any, ...]:
    mapper: Mapper = instance.__class__.__mapper__
    pk_cols = mapper.primary_key
    return tuple(getattr(instance, col.key) for col in pk_cols)

def serialize_arg(name: str, value: Any) -> str:
    if hasattr(value, "__mapper__"):
        pk = extract_pk(value)
        if len(pk) == 1:
            pk_repr = str(pk[0])
        else:
            pk_repr = "-".join(str(v) for v in pk)
        return f"{name}={pk_repr}"

    if isinstance(value, (list, tuple)):
        return f"{name}=" + "[" + ",".join(
            serialize_arg("", v).split("=")[-1] for v in value
        ) + "]"

    if isinstance(value, dict):
        ordered = sorted(value.items())
        items = ",".join(
            f"{k}:{serialize_arg('', v).split('=')[-1]}" for k, v in ordered
        )
        return f"{name}={{{ {items} }}}"

    return f"{name}={value}"


def build_cache_key(
    func: Callable[..., Any],
    args,
    kwargs
) -> str:

    parts: list[str] = []

    prefix: str = f"{func.__module__}.{func.__qualname__}"

    for i, arg in enumerate(args):
        parts.append(serialize_arg(f"arg{i}", arg))

    for key, value in sorted(kwargs.items()):
        parts.append(serialize_arg(key, value))

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


def init_cache(app: Flask) -> Cache:
    cache.init_app(app)
    return cache
