import streamlit as st
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent

def load_data():
    data = {
        "balance": 0,
        "total_deposited": 0,
        "total_withdrawn": 0
    }

    try:
        with open("data.txt", "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                data[key] = int(value)
    except FileNotFoundError:
        pass

    return data

def save_data(balance, total_dep, total_wit):
    with open("data.txt", "w") as file:
        file.write(f"balance={balance}\n")
        file.write(f"total_deposited={total_dep}\n")
        file.write(f"total_withdrawn={total_wit}\n")


with open("balance.txt", "r", encoding="utf-8") as f:
    st.session_state.balance = f.read()

if "show_history" not in st.session_state:
    st.session_state.show_history = False

with open("history.txt", "r", encoding="utf-8") as f:
    history = f.read()

if "total_deposited" not in st.session_state:
    st.session_state.total_deposited = 0

if "total_withdrawn" not in st.session_state:
    st.session_state.total_withdrawn = 0

st.markdown(
    f"""
    <p style='font-size:22px; color:#391560; font-weight:bold; text-align:center;'>
        Balance: {st.session_state.balance} $
    </p>
    """,
    unsafe_allow_html=True
)

money = st.number_input("Enter a number", min_value=0,step=1000)

def save_history(text):
    with open ("history.txt", "a") as file:
        file.write(text + "\n")

def see_history():
    try:
        with open ("history.txt", "r") as file:
            content = file.read()
        
            if (content.strip() == ""):
                st.error("There is not registred operations")
            else:
                st.code(content)
    except FileNotFoundError:
        st.info("History. There is not registred operations")

def deposit():
    global money
    
    if (money == 0):
        st.warning("Enter a valid number") 
    else:
        st.session_state.total_deposited += money
        st.session_state.balance = int(st.session_state.balance) + money
        save_data(st.session_state.balance, 
                  st.session_state.total_deposited, 
                  st.session_state.total_withdrawn)
        save_history(f"DEPOSIT: +{money} | ACTUAL BALANCE: {st.session_state.balance}")
        
def withdraw():
    global money
    if (money > int(st.session_state.balance)):
        st.warning("Not enough balance")
    elif (money == 0):
        st.warning("Enter a valid number")    
    else:
        st.session_state.balance = int(st.session_state.balance) - money
        st.session_state.total_withdrawn += money
        save_data(st.session_state.balance, 
                  st.session_state.total_deposited, 
                  st.session_state.total_withdrawn)
        save_history(f"WITHDRAW: -{money} | ACTUAL BALANCE: {st.session_state.balance}")

def save_balance(balance):
    with open("balance.txt", "w") as file:
        file.write(str(balance))

def clean_history():
        open("history.txt", "w").close()
        st.info("History successfully deleted")
 
if "initialized" not in st.session_state:
    data = load_data()

    st.session_state.balance = data["balance"]
    st.session_state.total_deposited = data["total_deposited"]
    st.session_state.total_withdrawn = data["total_withdrawn"]

    st.session_state.initialized = True
  
col1, col2, col3, col4 = st.columns(4)

with col1: 
    if st.button("Deposit"):
        deposit()
        save_balance(st.session_state.balance)

with col2:
    if st.button("Withdraw"):
        withdraw()
        save_balance(st.session_state.balance) 

with col3:
    if st.button("History"):
        st.session_state.show_history = not st.session_state.show_history
    
if st.session_state.show_history:
    see_history()

with col4:
    if st.button("Clean history"):
        clean_history()

col1_1, col2_1, col3_1 = st.columns(3)

with col1_1:
    st.metric("Current balance", f"${st.session_state.balance}")
    
with col2_1:
    st.metric("Total deposited", f"${st.session_state.total_deposited}") 
    
with col3_1:
    st.metric("Total withdrawn", f"${st.session_state.total_withdrawn}")

data = {
    "Metric": ["Balance", "Total Deposited", "Total Withdrawn"],
    "Amount": [
        st.session_state.balance,
        st.session_state.total_deposited,
        st.session_state.total_withdrawn
    ]
}

df = pd.DataFrame(data).set_index("Metric")

st.bar_chart(df)
