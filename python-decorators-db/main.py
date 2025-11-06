
from database.db_connection import init_db
from database.queries import get_all_users

if __name__ == "__main__":
    print("Initializing database...")
    init_db()

    print("\nFetching all users:")
    users = get_all_users()
    print(users)
