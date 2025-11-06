import sqlite3
from decorators import log_queries
from decorators.connection_decorator import with_connection
from decorators.transaction_decorator import transaction_manager

# Example: Function to create a users table
@with_connection("users.db")
@transaction_manager
@log_queries
def create_users_table(cursor=None, conn=None, **kwargs):
    """Create the users table if it doesn't already exist."""
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """
    kwargs["query"] = query
    cursor.execute(query)
    print("[INFO] Users table created successfully.")


# Example: Insert a new user into the database
@with_connection("users.db")
@transaction_manager
@log_queries
def insert_user(cursor=None, conn=None, name=None, email=None, **kwargs):
    """Insert a new user into the users table."""
    query = "INSERT INTO users (name, email) VALUES (?, ?)"
    kwargs["query"] = query
    cursor.execute(query, (name, email))
    print(f"[INFO] User '{name}' inserted successfully.")


# Example: Retrieve all users
@with_connection("users.db")
@log_queries
def fetch_all_users(cursor=None, conn=None, **kwargs):
    """Fetch all users from the database."""
    query = "SELECT * FROM users"
    kwargs["query"] = query
    cursor.execute(query)
    results = cursor.fetchall()
    print(f"[INFO] Retrieved {len(results)} users.")
    return results
