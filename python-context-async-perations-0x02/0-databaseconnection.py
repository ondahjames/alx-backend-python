import sqlite3

class DatabaseConnection:
    """Custom class-based context manager to handle database connections."""
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection."""
        self.conn = sqlite3.connect(self.db_name)
        print(f"[INFO] Connected to database: {self.db_name}")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection and handle exceptions."""
        if self.conn:
            self.conn.close()
            print(f"[INFO] Database connection closed: {self.db_name}")

        if exc_type:
            print(f"[ERROR] Exception occurred: {exc_val}")
        # Returning False will propagate the exception if needed
        return False


# Example usage
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()

        print("\n[RESULTS] User Records:")
        for row in results:
            print(row)
