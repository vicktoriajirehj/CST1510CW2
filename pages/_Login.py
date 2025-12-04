import streamlit as st
from database.db_manager import DatabaseManager
from database.crud import get_user_by_username
import bcrypt

st.title("🔐Login")

db = DatabaseManager()

# Determining session state to track login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

username = st.text_input("Username")
password = st.text_input("Password", type ="password")

if st.button("Login"):
    user = get_user_by_username(username)

    if user:
        _, db_username, db_hash, db_role = user[0]
        if verify_password(password, db_hash):
            st.session_state.logged_in = True
            st.session_state.role = db_role
            st.session_state.username = db_username
            st.success(f"Welcome {db_username}! Role: {db_role}")
        else:
            st.error("Incorrect password.")
    else:
        st.error("User not found")
