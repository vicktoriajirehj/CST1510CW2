import streamlit as st
import bcrypt
from database.auth import get_user_by_username, register_user

st.title("🔐 Login / Register")

# -----------------------------
# Initialize session state
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None

# -----------------------------
# Helper function
# -----------------------------
def verify_password(plain_password, hashed):
    """Check plaintext password against hashed password"""
    return bcrypt.checkpw(plain_password.encode(), hashed.encode())

# -----------------------------
# Tabs
# -----------------------------
tab = st.radio("Choose action", ["Login", "Register"])

# -----------------------------
# REGISTER
# -----------------------------
if tab == "Register":
    st.subheader(" Register New User")

    new_username = st.text_input("Username", key="reg_username")
    new_password = st.text_input("Password", type="password", key="reg_password")
    new_role = st.selectbox("Role", ["cyber", "it", "data"], key="reg_role")

    if st.button("Register", key="register_button"):
        success = register_user(new_username, new_password, new_role)
        if success:
            st.success("User registered successfully!")
        else:
            st.error("Username already exists!")
        if not new_username or not new_password:
            st.warning("Please enter both username and password.")
        elif get_user_by_username(new_username):
            st.error("Username already exists!")
        else:
            # Hash password before storing
            hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode('utf-8')
            register_user(new_username, hashed_pw, new_role)
            st.success(f"User '{new_username}' registered successfully!")

# -----------------------------
# LOGIN
# -----------------------------
if tab == "Login":
    st.subheader("🔑 Login")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        if not username or not password:
            st.warning("Please enter both username and password.")
        else:
            try:
                # Fetch user from DB
                user = get_user_by_username(username)

                if not user:
                    st.error("User not found.")
                else:
                    hashed_pw = user['password_hash']  # <- Updated column name

                    if verify_password(password, hashed_pw):
                        st.success(f"Welcome, {username}!")
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        st.session_state['role'] = user.get('role', None)
                    else:
                        st.error("Incorrect password.")

            except Exception as e:
                st.error(f"Database error: {e}")
                st.stop()

