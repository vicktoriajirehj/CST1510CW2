from db_manager import DatabaseManager
import os

USERS_FILE = "../users.txt"   # adjust if needed

db = DatabaseManager()

if not os.path.exists(USERS_FILE):
    print("No users.txt found. Nothing to migrate.")
    exit()

with open(USERS_FILE, "r") as f:
    for line in f:
        username, password_hash, role = line.strip().split(",")

        db.execute("""
            INSERT OR IGNORE INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (username, password_hash, role))

print("Users migrated successfully!")
db.close()
