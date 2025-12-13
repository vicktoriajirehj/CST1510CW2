import os
import pandas as pd
import bcrypt

# -----------------------
# CSV path configuration
# -----------------------
BASE_DIR = os.path.dirname(__file__)  # directory of auth.py
CSV_PATH = os.path.join(BASE_DIR, "csv_files", "users.csv")

# Ensure the CSV exists
if not os.path.exists(CSV_PATH):
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    pd.DataFrame(columns=["id", "username", "password_hash", "role"]).to_csv(CSV_PATH, index=False)

# -----------------------
# User functions
# -----------------------
def get_user_by_username(username):
    users_df = pd.read_csv(CSV_PATH)
    user_row = users_df[users_df["username"] == username]
    if user_row.empty:
        return None
    return user_row.iloc[0].to_dict()


def register_user(username, plain_password, role="user"):
    users_df = pd.read_csv(CSV_PATH)

    # Check if username exists
    if username in users_df['username'].values:
        return False

    # Hash the password
    hashed_pw = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    # Add new user
    new_id = users_df['id'].max() + 1 if not users_df.empty else 1
    new_user = {"id": new_id, "username": username, "password_hash": hashed_pw, "role": role}
    users_df = pd.concat([users_df, pd.DataFrame([new_user])], ignore_index=True)

    users_df.to_csv(CSV_PATH, index=False)
    return True


def verify_password(plain_password, hashed):
    return bcrypt.checkpw(plain_password.encode(), hashed.encode())
