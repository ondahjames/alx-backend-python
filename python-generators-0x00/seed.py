import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

# -----------------------------
# Function: Connect to MySQL Server
# -----------------------------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',       # Change if needed
            user='root',            # Your MySQL username
            password='yourpassword' # Your MySQL password
        )
        print("Connected to MySQL server")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# -----------------------------
# Function: Create Database
# -----------------------------
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev is ready")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()

# -----------------------------
# Function: Connect to ALX_prodev
# -----------------------------
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='yourpassword',
            database='ALX_prodev'
        )
        print("Connected to ALX_prodev database")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# -----------------------------
# Function: Create Table
# -----------------------------
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,2) NOT NULL,
        INDEX idx_user_id (user_id)
    )
    """
    try:
        cursor.execute(create_table_query)
        print("Table user_data is ready")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    finally:
        cursor.close()

# -----------------------------
# Function: Insert Data from CSV
# -----------------------------
def insert_data(connection, data):
    cursor = connection.cursor()
    insert_query = """
    INSERT IGNORE INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    try:
        for row in data:
            user_id = str(uuid.uuid4())  # Generate UUID
            name, email, age = row
            cursor.execute(insert_query, (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()

# -----------------------------
# Function: Load CSV Data
# -----------------------------
def load_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        return [row for row in reader]

# -----------------------------
# Main Script
# -----------------------------
if __name__ == "__main__":
    # Step 1: Connect to MySQL Server
    conn = connect_db()
    if conn is None:
        exit(1)

    # Step 2: Create Database
    create_database(conn)
    conn.close()

    # Step 3: Connect to ALX_prodev
    conn = connect_to_prodev()
    if conn is None:
        exit(1)

    # Step 4: Create Table
    create_table(conn)

    # Step 5: Load CSV and Insert Data
    csv_data = load_csv("user_data.csv")
    insert_data(conn, csv_data)

    conn.close()
