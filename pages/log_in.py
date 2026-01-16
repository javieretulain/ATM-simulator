import streamlit as st
from auth import register_user, login_user

st.markdown(
    """
    <p style='font-size:22px; color:#391560; font-weight:bold; text-align:center;'>
        Welcome to the Banking App!
    </p>
    """,
    unsafe_allow_html=True
)

@st.dialog("Log in")
def log_in():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        user = login_user(email, password)

        if user:
            user_id, balance = user
            st.session_state.user_id = user_id
            st.session_state.balance = balance
            st.success("Logged in successfully")
            st.switch_page("app.py")
        else:
            st.error("Invalid email or password")

@st.dialog("Sign up")
def sign_up():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    conf_password = st.text_input("Confirm Password", type="password")

    if st.button("Create account"):
        if password != conf_password:
            st.error("Passwords do not match")
            return

        if register_user(email, password):
            st.success("Account created successfully")
        else:
            st.error("Email already registered")
col_spc1, col_btn1, col_spc2 = st.columns([3,1,3])
col_spc3, col_btn2, col_spc4 = st.columns([3,1,3])

with col_btn1:
    if st.button("Log In"):
        log_in()

with col_btn2:
    if st.button("Sign Up"):
        sign_up()
