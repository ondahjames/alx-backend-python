#!/usr/bin/python3
"""Implements lazy pagination using generators."""

import mysql.connector

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )


def paginate_users(page_size, offset):
    """
    Fetches a page of users from the user_data table based on page size and offset.
    """
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator function that yields user pages lazily.
    Fetches the next page only when needed.
    Uses only one loop.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break  # stop when there are no more results
        yield page  # ✅ use yield to return each page lazily
        offset += page_size  # move to the next offset


# Optional: test behavior
if __name__ == "__main__":
    for page in lazy_paginate(5):
        print(f"Fetched {len(page)} users:")
        for user in page:
            print(user)
