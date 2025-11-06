# decorators/transaction_decorator.py
from functools import wraps

def transaction_manager(func):
    """Decorator to manage database transactions (commit/rollback)."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = kwargs.get('conn', None)
        if not conn:
            raise ValueError("[ERROR] No database connection found. Ensure connection decorator is used.")

        try:
            print("[TRANSACTION] Starting new transaction.")
            result = func(*args, **kwargs)
            conn.commit()
            print("[TRANSACTION] Transaction committed successfully.")
            return result

        except Exception as e:
            conn.rollback()
            print(f"[TRANSACTION] Rolled back due to error: {e}")
            raise

    return wrapper
