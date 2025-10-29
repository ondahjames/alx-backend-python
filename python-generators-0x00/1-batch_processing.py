import mysql.connector

# -----------------------------
# Function: Stream Users in Batches
# -----------------------------
def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows from user_data table in batches.
    :param batch_size: Number of rows to fetch per batch
    :yield: List of rows (dictionaries)
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

        batch = []
        # Single loop: iterate through all rows
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch  # Yield full batch
                batch = []   # Reset batch

        # Yield any remaining rows in the last batch
        if batch:
            yield batch

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# -----------------------------
# Function: Process Batches
# -----------------------------
def batch_processing(batch_size):
    """
    Processes each batch of users to filter those over the age of 25.
    :param batch_size: Number of rows per batch
    :yield: Filtered users over 25
    """
    # Loop 1: iterate through batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 2: iterate through users in batch
        filtered_batch = [user for user in batch if float(user['age']) > 25]
        # Loop 3 is optional if you yield individual users
        for user in filtered_batch:
            yield user


# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    batch_size = 5  # Example batch size

    print("Filtered users over age 25:")
    for user in batch_processing(batch_size):
        print(user)
