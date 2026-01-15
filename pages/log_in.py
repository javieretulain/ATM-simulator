from distro import name
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).parent

@st.dialog("Log in")
def log_in():
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Submit"):
        st.success("Logged in successfully!")

@st.dialog("Sign up")
def sign_up():
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    conf_password = st.text_input("Confirm Password", type="password")
    if st.button("Submit"):
        if password != conf_password:
            st.error("Passwords do not match!")
        else:
            st.success("Account created successfully!")
    
st.markdown(
    f"""
    <p style='font-size:22px; color:#391560; font-weight:bold; text-align:center;'>
        Welcome to the Banking App!
    </p>
    """,
    unsafe_allow_html=True
)

col_spc1, col_btn, col_spc2 = st.columns([3,1,3])
col_spc3, col_btn2, col_spc4 = st.columns([3,1,3])

with col_btn:
    if st.button("Log In"):
        log_in()
        st.success("Logged in successfully!")

with col_btn2:
    if st.button("Sign Up"):
        sign_up()
        st.success("Account created successfully!")
