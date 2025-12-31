# backend/app/test_db_connection.py

print("🔹 test_db_connection.py started")  # DEBUG

from sqlalchemy import text
from .db import engine

print("🔹 Imported engine from app.db")  # DEBUG


def main():
    print("🔹 Inside main(), trying to connect...")  # DEBUG
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database(), current_user;"))
            db_name, db_user = result.fetchone()
            print("✅ Connected to DB:", db_name, "as user:", db_user)
    except Exception as e:
        print("❌ Failed to connect to DB:", e)


if __name__ == "__main__":
    print("🔹 __name__ == '__main__', calling main()")  # DEBUG
    main()