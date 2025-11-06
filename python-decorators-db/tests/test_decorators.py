from database.db_connection import init_db
from database.queries import get_all_users

def test_query_execution():
    init_db()
    try:
        users = get_all_users()
        assert isinstance(users, list)
        print("Test passed ✅")
    except Exception as e:
        print(f"Test failed ❌: {e}")
