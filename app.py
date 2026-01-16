import streamlit as st
import pandas as pd
from database import init_db, get_connection

init_db()

if "user_id" not in st.session_state:
    st.switch_page("pages/log_in.py")

user_id = st.session_state.user_id

def get_user_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT balance FROM users WHERE id=?",
        (user_id,)
    )
    balance = cur.fetchone()[0]

    cur.execute(
        "SELECT SUM(amount) FROM history WHERE user_id=? AND operation='DEPOSIT'",
        (user_id,)
    )
    total_deposited = cur.fetchone()[0] or 0

    cur.execute(
        "SELECT SUM(amount) FROM history WHERE user_id=? AND operation='WITHDRAW'",
        (user_id,)
    )
    total_withdrawn = cur.fetchone()[0] or 0

    conn.close()
    return balance, total_deposited, total_withdrawn

def update_balance(new_balance):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET balance=? WHERE id=?",
        (new_balance, user_id)
    )

    conn.commit()
    conn.close()

def save_history(operation, amount, balance_after):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO history (user_id, operation, amount, balance_after)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, operation, amount, balance_after)
    )

    conn.commit()
    conn.close()

def get_history():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT operation, amount, balance_after, created_at
        FROM history
        WHERE user_id=?
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    rows = cur.fetchall()
    conn.close()
    return rows

def clean_history():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM history WHERE user_id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

balance, total_deposited, total_withdrawn = get_user_data()

st.markdown(
    f"""
    <p style='font-size:22px; color:#391560; font-weight:bold; text-align:center;'>
        Balance: ${balance}
    </p>
    """,
    unsafe_allow_html=True
)

money = st.number_input("Enter a number", min_value=0, step=1000)

def deposit():
    if money == 0:
        st.warning("Enter a valid number")
        return

    new_balance = balance + money
    update_balance(new_balance)
    save_history("DEPOSIT", money, new_balance)
    st.success("Deposit successful")
    st.rerun()

def withdraw():
    if money == 0:
        st.warning("Enter a valid number")
        return

    if money > balance:
        st.warning("Not enough balance")
        return

    new_balance = balance - money
    update_balance(new_balance)
    save_history("WITHDRAW", money, new_balance)
    st.success("Withdraw successful")
    st.rerun()

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Deposit"):
        deposit()

with col2:
    if st.button("Withdraw"):
        withdraw()

with col3:
    if st.button("History"):
        st.session_state.show_history = not st.session_state.get("show_history", False)

with col4:
    if st.button("Clean history"):
        clean_history()
        st.success("History deleted")
        st.rerun()

if st.session_state.get("show_history", False):
    history = get_history()

    if not history:
        st.info("No registered operations")
    else:
        df_hist = pd.DataFrame(
            history,
            columns=["Operation", "Amount", "Balance After", "Date"]
        )
        st.dataframe(df_hist, use_container_width=True)

col1_1, col2_1, col3_1 = st.columns(3)

with col1_1:
    st.metric("Current balance", f"${balance}")

with col2_1:
    st.metric("Total deposited", f"${total_deposited}")

with col3_1:
    st.metric("Total withdrawn", f"${total_withdrawn}")

df_chart = pd.DataFrame({
    "Amount": [balance, total_deposited, total_withdrawn]
}, index=["Balance", "Total Deposited", "Total Withdrawn"])

st.bar_chart(df_chart)
