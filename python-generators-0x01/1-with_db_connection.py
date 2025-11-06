import sqlite3
import functools

def with_db_connection(func):
    """Decorator that opens a database connection, passes it to the function, and closes it afterward."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            # Open connection
            conn = sqlite3.connect("users.db")
            print("[INFO] Database connection opened.")
            
            # Pass connection into the decorated function
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


@with_db_connection
def get_user_by_id(conn, user_id):
    """Fetch user record by ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
