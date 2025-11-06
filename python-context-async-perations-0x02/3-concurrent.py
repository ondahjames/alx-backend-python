import asyncio
import aiosqlite

# Asynchronous function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("\n[ALL USERS]")
            for row in results:
                print(row)
            return results


# Asynchronous function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("\n[USERS OLDER THAN 40]")
            for row in results:
                print(row)
            return results


# Main coroutine to run both concurrently
async def fetch_concurrently():
    # Run both functions concurrently using asyncio.gather
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("\n[SUMMARY]")
    print(f"Fetched {len(results[0])} total users.")
    print(f"Fetched {len(results[1])} users older than 40.")


# Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
