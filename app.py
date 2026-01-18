import streamlit as st
import pandas as pd
import altair as alt
from database import get_connection

if not st.session_state.get("user_id"):
    st.switch_page("pages/log_in.py")

user_id = st.session_state.user_id

with st.sidebar:
    st.write("✅ Logged in")
    st.write(f"User ID: {user_id}")
    if st.button("Logout"):
        del st.session_state["user_id"]
        st.switch_page("pages/log_in.py")

def get_user_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT balance FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    if row is None:
        return 0, 0, 0, 0, 0
    balance = row[0]

    cur.execute(
        "SELECT COALESCE(SUM(amount),0) FROM history WHERE user_id=%s AND operation='DEPOSIT'",
        (user_id,)
    )
    total_deposited = cur.fetchone()[0]

    cur.execute(
        "SELECT COALESCE(SUM(amount),0) FROM history WHERE user_id=%s AND operation='WITHDRAW'",
        (user_id,)
    )
    total_withdrawn = cur.fetchone()[0]

    cur.execute(
        "SELECT COALESCE(SUM(amount),0) FROM history WHERE user_id=%s AND operation='TRANSFER IN'",
        (user_id,)
    )
    total_transfers_in = cur.fetchone()[0]

    cur.execute(
        "SELECT COALESCE(SUM(amount),0) FROM history WHERE user_id=%s AND operation='TRANSFER OUT'",
        (user_id,)
    )
    total_transfers_out = cur.fetchone()[0]

    conn.close()
    return balance, total_deposited, total_withdrawn, total_transfers_in, total_transfers_out

def update_balance(new_balance):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET balance=%s WHERE id=%s",
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
        VALUES (%s, %s, %s, %s)
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
        WHERE user_id=%s
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
    cur.execute("DELETE FROM history WHERE user_id=%s", (user_id,))
    conn.commit()
    conn.close()

balance, total_deposited, total_withdrawn, total_transfers_in, total_transfers_out = get_user_data()

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
    if money <= 0:
        st.warning("Enter a valid number")
        return
    new_balance = balance + money
    update_balance(new_balance)
    save_history("DEPOSIT", money, new_balance)
    st.success("Deposit successful")

def withdraw():
    if money <= 0:
        st.warning("Enter a valid number")
        return
    if money > balance:
        st.warning("Not enough balance")
        return
    new_balance = balance - money
    update_balance(new_balance)
    save_history("WITHDRAW", money, new_balance)
    st.success("Withdraw successful")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button("Deposit", on_click=deposit)

with col2:
    st.button("Withdraw", on_click=withdraw)

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
    if history:
        df_hist = pd.DataFrame(
            history,
            columns=["Operation", "Amount", "Balance After", "Date"]
        )
        st.dataframe(df_hist, use_container_width=True)
    else:
        st.info("No registered operations")

col1_1, col2_1, col3_1, col4_1, col5_1 = st.columns(5)

with col1_1:
    st.metric("Current balance", f"${balance}")
with col2_1:
    st.metric("Total deposited", f"${total_deposited}")
with col3_1:
    st.metric("Total withdrawn", f"${total_withdrawn}")
with col4_1:
    st.metric("Total transfers in", f"${total_transfers_in}")
with col5_1:
    st.metric("Total transfers out", f"${total_transfers_out}")

chart_df = pd.DataFrame({
    "Category": [
        "Balance",
        "Total deposited",
        "Total withdrawn",
        "Total transfers in",
        "Total transfers out"
    ],
    "Amount": [
        balance,
        total_deposited,
        total_withdrawn,
        total_transfers_in,
        total_transfers_out
    ]
})

chart = (
    alt.Chart(chart_df)
    .mark_bar()
    .encode(
        x=alt.X(
            "Category:N",
            sort=[
                "Balance",
                "Total deposited",
                "Total withdrawn",
                "Total transfers in",
                "Total transfers out"
            ]
        ),
        y="Amount:Q"
    )
)

st.altair_chart(chart, use_container_width=True)
