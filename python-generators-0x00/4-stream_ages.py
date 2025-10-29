#!/usr/bin/python3
"""Compute average user age using a generator without loading the full dataset."""

import mysql.connector


def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )


def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    Uses yield to avoid loading all data into memory.
    """
    conn = connect_to_prodev()
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield age  # ✅ yield one age at a time

    cursor.close()
    conn.close()


def calculate_average_age():
    """
    Calculates the average age of users using the generator.
    Only iterates through the dataset once.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += float(age)
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    calculate_average_age()
