import time
import sqlite3
import functools


# -------------------------------
# Database Connection Decorator
# -------------------------------
def with_db_connection(func):
    """Decorator that opens a database connection, passes it to the function, and closes it afterward."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect("users.db")
            print("[INFO] Database connection opened.")
            
            result = func(conn, *args, **kwargs)
            return result
        
        except sqlite3.Error as e:
            print(f"[ERROR] Database operation failed: {e}")
            raise
        
        finally:
            if conn:
                conn.close()
                print("[INFO] Database connection closed.")
    
    return wrapper


# -------------------------------
# Retry Decorator
# -------------------------------
def retry_on_failure(retries=3, delay=2):
    """Decorator that retries a function if it fails due to transient errors."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    print(f"[RETRY] Attempt {attempt + 1} of {retries}")
                    return func(*args, **kwargs)
                except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
                    print(f"[WARNING] Operation failed: {e}")
                    attempt += 1
                    if attempt < retries:
                        print(f"[INFO] Retrying in {delay} seconds...\n")
                        time.sleep(delay)
                    else:
                        print("[ERROR] All retry attempts failed.")
                        raise
        return wrapper
    return decorator


# -------------------------------
# Example Function Using Both Decorators
# -------------------------------
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """Fetch all users, retrying on failure."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# -------------------------------
# Run the Function
# -------------------------------
if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        print("[SUCCESS] Users fetched successfully!")
        print(users)
    except Exception as e:
        print(f"[FAILED] Could not fetch users: {e}")
