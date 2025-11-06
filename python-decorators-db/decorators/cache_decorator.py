# decorators/cache_decorator.py
from functools import wraps

def cache_results(func):
    """Decorator to cache results of database queries to optimize performance."""
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Build a unique key from function name + arguments
        key = (func.__name__, args, frozenset(kwargs.items()))

        if key in cache:
            print(f"[CACHE] Returning cached result for {func.__name__}{args}")
            return cache[key]

        print(f"[CACHE] No cache found for {func.__name__}{args}. Executing query...")
        result = func(*args, **kwargs)
        cache[key] = result
        print(f"[CACHE] Cached result for {func.__name__}{args}")
        return result

    return wrapper
