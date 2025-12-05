import sys
import os
import streamlit as st
import bcrypt

# -----------------------------
# Fix for Streamlit pages import
# -----------------------------
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# -----------------------------
# Imports from database
# -----------------------------
from database.db_manager import DatabaseManager, get_user_by_username, register_user

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🔐 Login / Register")

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
    """Verify a password against a stored hash"""
    return bcrypt.checkpw(password.encode(), hashed.encode())

# -----------------------------
# Tabs for Login and Register
# -----------------------------
tab = st.radio("Choose action", ["Login", "Register"])

# -----------------------------
# REGISTER
# -----------------------------
if tab == "Register":
    st.subheader("📋 Register New User")
    new_username = st.text_input("Username", key="reg_user")
    new_password = st.text_input("Password", type="password", key="reg_pass")
    new_role = st.selectbox("Role", ["cyber", "it", "data"], key="reg_role")

    if st.button("Register"):
        if get_user_by_username(new_username):
            st.error("Username already exists!")
        else:
            register_user(new_username, new_password, new_role)
            st.success(f"User '{new_username}' registered successfully!")

# -----------------------------
# LOGIN
# -----------------------------
elif tab == "Login":
    st.subheader("🔐 Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        user = get_user_by_username(username)
        if user:
            _, db_username, db_hash, db_role = user[0]
            if verify_password(password, db_hash):
                st.session_state.logged_in = True
                st.session_state.username = db_username
                st.session_state.role = db_role
                st.success(f"Welcome {db_username}! Role: {db_role}")
            else:
                st.error("Incorrect password.")
        else:
            st.error("User not found.")
