import psycopg2
import streamlit as st

def get_connection():
    try:
        conn = psycopg2.connect(
            host=st.secrets["db_host"],
            database=st.secrets["db_name"],
            user=st.secrets["db_user"],
            password=st.secrets["db_password"],
            port=st.secrets["db_port"],
            sslmode="require"
        )
        return conn
    except Exception as e:
        import streamlit as st
        st.error(str(e))
        raise
