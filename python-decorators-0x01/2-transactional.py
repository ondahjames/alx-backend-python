def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            print("[INFO] Database connection opened.")
            result = func(conn, *args, **kwargs)
            conn.commit()  # ✅ Commit only if no errors
            return result
        except sqlite3.Error as e:
            print(f"[ERROR] Database operation failed: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
            print("[INFO] Database connection closed.")
    return wrapper
