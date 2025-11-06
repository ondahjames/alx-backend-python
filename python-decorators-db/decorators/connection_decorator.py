# decorators/connection_decorator.py
import sqlite3
from functools import wraps

def with_connection(db_name="users.db"):
    """Decorator to handle database connection automatically."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            conn = None
            try:
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                print(f"[DB] Connection to {db_name} established.")
                
                # Inject connection and cursor into the function
                result = func(cursor=cursor, conn=conn, *args, **kwargs)
                
                conn.commit()
                print("[DB] Changes committed successfully.")
                return result

            except Exception as e:
                if conn:
                    conn.rollback()
                    print(f"[DB] Transaction rolled back due to error: {e}")
                raise

            finally:
                if conn:
                    conn.close()
                    print("[DB] Connection closed.")

        return wrapper
    return decorator
