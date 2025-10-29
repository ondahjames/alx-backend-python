import mysql.connector

# -----------------------------
# Function: Stream Users
# -----------------------------
def stream_users():
    """
    Generator function that fetches rows one by one from user_data table.
    Yields each row as a dictionary.
    """
    try:
        # Connect to ALX_prodev database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='yourpassword',  # Replace with your MySQL password
            database='ALX_prodev'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        # Single loop: fetch and yield rows one by one
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    for user in stream_users():
        print(user)
