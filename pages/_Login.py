import sys
import os

# -----------------------------
# Fix for Streamlit pages import
# -----------------------------
# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# -----------------------------
# Standard imports
# -----------------------------
import streamlit as st
from database.db_manager import DatabaseManager
from database.crud import get_user_by_username
import bcrypt

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🔐 Login")

# Initialize database manager
db = DatabaseManager()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None

# -----------------------------
# Password verification function
# -----------------------------
def verify_password(password, hashed):
    """
    Verify a plain password against a hashed password
    """
    return bcrypt.checkpw(password.encode(), hashed.encode())

# -----------------------------
# Input fields
# -----------------------------
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# -----------------------------
# Login button logic
# -----------------------------
if st.button("Login"):
    user = get_user_by_username(username)

    if user:
        # Assuming your user tuple
        _, db_username, db_hash, db_role = user[0]

        if verify_password(password, db_hash):
            st.session_state.logged_in = True
            st.session_state.role = db_role
            st.session_state.username = db_username
            st.success(f"Welcome {db_username}! Role: {db_role}")
        else:
            st.error("Incorrect password.")
    else:
        st.error("User not found."
