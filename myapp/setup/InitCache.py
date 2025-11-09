from flask import Flask
from flask_caching import Cache

cache = Cache()
redis_conn = None

def init_cache(app: Flask) -> Cache:
    cache.init_app(app)

    return cache
