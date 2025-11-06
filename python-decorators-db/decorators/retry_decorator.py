# decorators/retry_decorator.py
from functools import wraps
import time

def retry_on_failure(retries=3, delay=2):
    """Decorator to retry database operations on transient failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, retries + 1):
                try:
                    print(f"[RETRY] Attempt {attempt}/{retries} for {func.__name__}")
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"[ERROR] Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"[RETRY] Waiting {delay} seconds before retrying...")
                        time.sleep(delay)
                    else:
                        print("[RETRY] All attempts failed. Raising last exception.")
                        raise last_exception

        return wrapper
    return decorator
