import streamlit as st
from pathlib import Path
from database import get_connection

BASE_DIR = Path(__file__).parent

if "user_id" not in st.session_state:
    st.switch_page("pages/log_in.py")

user_id = st.session_state.user_id

with st.sidebar:
    st.write("✅ Logged in")
    st.write(f"User ID: {user_id}")
    if st.button("Logout"):
        del st.session_state["user_id"]
        st.switch_page("pages/log_in.py")

transfer_amount = st.number_input("Transfer amount", min_value=0, key="transfer_amount", step=1000)

def make_transfer():
    amount = st.session_state.transfer_amount
    recipient_id = st.session_state.get("recipient_id")
    
    if not recipient_id:
        st.error("Recipient ID is required")
        return
    
    if amount <= 0:
        st.error("Transfer amount must be greater than zero")
        return

    conn = get_connection()
    cur = conn.cursor()

    # Check if user has sufficient balance
    cur.execute("SELECT balance FROM users WHERE id=%s", (user_id,))
    current_balance = cur.fetchone()[0]

    if amount > current_balance:
        st.error("Insufficient balance for this transfer")
        conn.close()
        return

    # Deduct amount from user's balance
    new_balance = current_balance - amount
    cur.execute("UPDATE users SET balance=%s WHERE id=%s", (new_balance, user_id))
    
    cur.execute("SELECT balance FROM users WHERE id=%s", (recipient_id,))
    row = cur.fetchone()

    if row is None:
        st.error("Recipient not found")
        conn.close()
        return

    recipient_balance = row[0]
    
    new_recipient_balance = recipient_balance + amount
    cur.execute(
    "UPDATE users SET balance=%s WHERE id=%s",
    (new_recipient_balance, recipient_id)
    )
    
    # Log the transfer in history
    cur.execute(
        """
        INSERT INTO history (user_id, operation, amount, balance_after)
        VALUES (%s, 'TRANSFER OUT', %s, %s)
        """,
        (user_id, amount, new_balance)
    )

    cur.execute(
        """
        INSERT INTO history (user_id, operation, amount, balance_after)
        VALUES (%s, 'TRANSFER IN', %s, %s)
        """,
        (recipient_id, amount, new_recipient_balance)
    )

    conn.commit()
    conn.close()

    st.success(f"Successfully transferred {amount}. New balance is {new_balance}.")

st.text_input("Enter the ID of the recipient", key="recipient_id")

if st.button("Make Transfer"):
    make_transfer()