import streamlit as st

with open("balance.txt", "r", encoding="utf-8") as f:
    inity_balance = f.read()

if "show_history" not in st.session_state:
    st.session_state.show_history = False

with open("history.txt", "r", encoding="utf-8") as f:
    history = f.read()

st.markdown(
    f"""
    <p style='font-size:22px; color:#44241A; font-weight:bold; text-align:center;'>
        Balance: {inity_balance}
    </p>
    """,
    unsafe_allow_html=True
)

money = int(st.number_input("Enter a number", min_value=0,step=1000))

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
    global inity_balance
    global money
    
    if (money == 0):
        st.warning("Enter a valid number") 
    else:
        inity_balance = int(inity_balance) + money
        save_history(f"DEPOSIT: +{money} | ACTUAL BALANCE: {inity_balance}")

def withdraw():
    global inity_balance
    global money
    if (money > int(inity_balance)):
        st.warning("Not enough balance")
    elif (money == 0):
        st.warning("Enter a valid number")    
    else:
        inity_balance = int(inity_balance) - money
        save_history(f"WITHDRAW: -{money} | ACTUAL BALANCE: {inity_balance}")

def save_balance(balance):
    with open("balance.txt", "w") as file:
        file.write(str(balance))

def clean_history():
        open("history.txt", "w").close()
        st.info("History successfully deleted")
   
col1, col2, col3, col4 = st.columns(4)

with col1: 
    if st.button("Deposit"):
        deposit()
        save_balance(inity_balance)

with col2:
    if st.button("Withdraw"):
        withdraw()
        save_balance(inity_balance) 

with col3:
    if st.button("History"):
        st.session_state.show_history = not st.session_state.show_history
    
if st.session_state.show_history:
    see_history()

with col4:
    if st.button("Clean history"):
        clean_history()

