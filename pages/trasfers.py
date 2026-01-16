import streamlit as st
from pathlib import Path
from database import get_connection

BASE_DIR = Path(__file__).parent

st.write("This is the Transfers page.")
