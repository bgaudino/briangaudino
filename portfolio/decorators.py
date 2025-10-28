from functools import wraps

from django.core.cache import cache


def cache_result(cache_key):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            result = func(*args, **kwargs)
            if cache_key:
                cache.set(cache_key, result)
            return result

        return wrapper

    return decorator
