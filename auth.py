import bcrypt
import os

USERS_FILE = "users.txt"

class User:
    def __init__(self, username: str, password_hash: bytes, role: str):
        self.username = username
        self.password_hash = password_hash
        self.role = role
def hash_password(password: str) -> bytes:
    """Hash a password with bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    """Verify a password against a stored hash."""
    return bcrypt.checkpw(password.encode(), hashed)

def load_users():
    """Return a list of Users from the users.txt file."""
    users = []
    if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                for line in f:
                    username, hashed, role = line.strip().split(",")
                    users.append(User(username, hashed.encode(), role))
    return users

def user_exists(username: str) -> bool:
    """Check if a user exists in the users file."""
    users = load_users()
    return any(user.username == username for user in users)

def register_user(username: str, password: str, role: str):
    if not username.strip():
        print("Username cannot be empty.")
        return
    if len(password) < 8:
        print("Password must be at least 8 characters.")
        return
    if role not in ["cyber", "it", "data"]:
        print("Invalid role. Role must be: cyber, data, or it")
        return
    if user_exists(username):
        print(f"Username '{username}' already exists. Choose a different username")
        return

    hashed = hash_password(password)
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{hashed.decode()},{role}\n")

    print(f"User '{username}' registered successfully.")


def login_user(username: str, password: str):
    users = load_users()

    for user in users:
        if user.username == username:
            if verify_password(password, user.password_hash()):
                print(f"Login successful! Welcome, {username}. Role: {user.role}")
                return True
            else:
                print("Incorrect password.")
                return False
    print("User not found.")
    return False


# Simple command-line interface
def menu():
    while True:
        print("\n=== Authentication Menu ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

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

        elif choice == "3":
            print("Exiting program...")
            break

        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()