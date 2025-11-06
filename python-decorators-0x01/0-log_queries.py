import sqlite3
import functools
from datetime import datetime   # ✅ Required import

def log_queries(func):
    """Decorator to log SQL queries executed by a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", None)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{timestamp}] Executing function: {func.__name__}")
        if query:
            print(f"[SQL] Query: {query}")

        # Execute the function
        result = func(*args, **kwargs)

        # Log query details to file
        with open("query_logs.txt", "a") as log_file:
            log_file.write(f"{timestamp} | Function: {func.__name__} | Query: {query}\n")

        print(f"[{timestamp}] Execution completed.\n")
        return result

    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
users = fetch_all_users(query="SELECT * FROM users")
print(users)
