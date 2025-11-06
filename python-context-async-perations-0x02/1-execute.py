import sqlite3

class ExecuteQuery:
    """Reusable context manager for executing database queries."""
    
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Open the database connection and execute the query."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"[INFO] Connected to database: {self.db_name}")

        # Execute query
        self.cursor.execute(self.query, self.params)
        results = self.cursor.fetchall()
        return results  # This is what 'as' will capture

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure connection is properly closed."""
        if self.conn:
            self.conn.close()
            print(f"[INFO] Database connection closed: {self.db_name}")

        if exc_type:
            print(f"[ERROR] Exception occurred: {exc_val}")
        # Returning False allows exceptions to propagate
        return False


# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        print("\n[RESULTS] Users older than 25:")
        for row in results:
            print(row)
