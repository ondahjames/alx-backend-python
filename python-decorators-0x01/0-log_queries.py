import sqlite3
import functools
import time


# -------------------------------
# Decorator to Log SQL Queries
# -------------------------------
def log_queries(func):
    """Decorator that logs SQL queries before executing them."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        start_time = time.time()

        print(f"[LOG] Function: {func.__name__}")
        print(f"[SQL] Executing Query: {query}")

        result = func(*args, **kwargs)

        duration = round((time.time() - start_time) * 1000, 2)
        print(f"[LOG] Execution completed in {duration}ms\n")

        # Optional: write logs to a file
        with open("query_logs.txt", "a") as f:
            f.write(f"{time.ctime()} | {func.__name__} | {query} | {duration}ms\n")

        return result

    return wrapper


# -------------------------------
# Example Function Using Decorator
# -------------------------------
@log_queries
def fetch_all_users(query):
    """Fetch all users from the database."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# -------------------------------
# Run Example
# -------------------------------
users = fetch_all_users(query="SELECT * FROM users")
print(users)
