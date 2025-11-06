import time
from functools import wraps

def log_queries(func):
    """Decorator to log SQL queries executed by a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", None)
        start_time = time.time()

        print(f"[LOG] Executing function: {func.__name__}")
        if query:
            print(f"[SQL] Query: {query}")  # fixed: removed typo 'acprint'

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(f"[ERROR] {func.__name__} failed: {e}")
            raise
        finally:
            end_time = time.time()
            duration = round((end_time - start_time) * 1000, 2)
            log_message = f"{func.__name__} | Query: {query} | Time: {duration}ms\n"
