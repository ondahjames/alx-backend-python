#!/usr/bin/python3
"""Stream and batch process users using generators."""

import mysql.connector

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )


def stream_users_in_batches(batch_size):
    """Yields batches of users from user_data table."""
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch  # ✅ yields batch, not return
            batch = []
    if batch:
        yield batch  # ✅ yields remaining rows

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """Processes each batch and yields users over age 25."""
    for batch in stream_users_in_batches(batch_size):
        filtered = [user for user in batch if user["age"] > 25]
        yield filtered  # ✅ yields filtered results, no return


# Optional: for testing the generator behavior
if __name__ == "__main__":
    for group in batch_processing(5):
        print(group)
