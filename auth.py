import bcrypt
import os

USERS_FILE = "users.txt"


def hash_password(password: str) -> bytes:
    """Hash a password with bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    """Verify a password against a stored hash."""
    return bcrypt.checkpw(password.encode(), hashed)


def register_user(username: str, password: str, role: str):
    hashed = hash_password(password)
    line = f"{username},{hashed.decode()},{role}\n"

    with open(USERS_FILE, "a") as f:
        f.write(line)

    print(f"User '{username}' registered successfully!")


def login_user(username: str, password: str):
    if not os.path.exists(USERS_FILE):
        print("No users registered yet.")
        return False

    with open(USERS_FILE, "r") as f:
        for line in f:
            saved_username, saved_hash, saved_role = line.strip().split(",")
            if username == saved_username:
                if verify_password(password, saved_hash.encode()):
                    print(f"Login successful! Role: {saved_role}")
                    return True
                else:
                    print("Incorrect password.")
                    return False

    print("User not found.")
    return False


# Simple command-line interface
if __name__ == "__main__":
    print("Choose an option:")
    print("1. Register")
    print("2. Login")

    choice = input("Enter choice: ")

    if choice == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")
        role = input("Enter role (cyber/data/it): ")
        register_user(username, password, role)

    elif choice == "2":
        username = input("Username: ")
        password = input("Password: ")
        login_user(username, password)
