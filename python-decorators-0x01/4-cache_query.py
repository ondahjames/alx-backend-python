import time
import sqlite3
import functools

# -------------------------------
# Query Cache Dictionary
# -------------------------------
query_cache = {}


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
# Cache Query Decorator
# -------------------------------
def cache_query(func):
    """Decorator that caches query results to avoid redundant DB calls."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[1] if len(args) > 1 else None)

        if query in query_cache:
            print(f"[CACHE] Using cached result for query: {query}")
            return query_cache[query]

        print(f"[CACHE MISS] Executing query for the first time: {query}")
        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"[CACHE] Query result cached.")
        return result

    return wrapper


# -------------------------------
# Example Function Using Decorators
# -------------------------------
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users from DB, caching results."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# -------------------------------
# Test Caching Behavior
# -------------------------------
if __name__ == "__main__":
    # First call — executes query and caches result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call — uses cache instead of hitting DB again
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
