
import streamlit as st
from bank_backend_v2 import Bank


# ---------------- PAGE SETUP ----------------

st.set_page_config(
    page_title="MyBank V2",
    page_icon="🏦",
    layout="wide"
)

# Create the bank object
if "bank" not in st.session_state:
    st.session_state.bank = Bank()

bank = st.session_state.bank


# ---------------- SIDEBAR ----------------

st.sidebar.title("🏦 MyBank V2")
st.sidebar.write("Bank Management System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Check Balance",
        "Account Details",
        "Update Details"
    ]
)


# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.title("Welcome to MyBank V2 👋")
    st.write("Manage your bank accounts easily.")

    total_accounts = len(bank.data)
    total_balance = 0

    for account in bank.data:
        total_balance += account["balance"]

    col1, col2 = st.columns(2)

    col1.metric("Total Accounts", total_accounts)
    col2.metric("Total Account Balances", f"₹{total_balance:,.2f}")

    st.divider()
    st.subheader("Available Services")

    col1, col2, col3 = st.columns(3)

    col1.info("👤 Create an account")
    col2.info("💰 Deposit or withdraw money")
    col3.info("📋 View or update account details")


# ---------------- CREATE ACCOUNT ----------------

elif page == "Create Account":

    st.title("👤 Create a Bank Account")

    with st.form("create_account_form"):

        name = st.text_input("Full Name")

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=18
        )

        email = st.text_input("Email Address")

        pin = st.text_input(
            "Create a 4-digit PIN",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Create Account",
            type="primary"
        )

    if submitted:

        success, result = bank.create_account(
            name, int(age), email, pin
        )

        if success:
            st.success("Account created successfully!")
            st.write("Your account number:")
            st.code(result)
            st.warning("Please save your account number.")

        else:
            st.error(result)


# ---------------- DEPOSIT MONEY ----------------

elif page == "Deposit Money":

    st.title("💰 Deposit Money")

    with st.form("deposit_form"):

        account_no = st.text_input("Account Number")
        pin = st.text_input("4-digit PIN", type="password")

        amount = st.number_input(
            "Deposit Amount (₹)",
            min_value=0,
            max_value=10000,
            value=100,
            step=100
        )

        submitted = st.form_submit_button(
            "Deposit Money",
            type="primary"
        )

    if submitted:

        success, result = bank.deposit_money(
            account_no, pin, int(amount)
        )

        if success:
            st.success("Deposit successful!")
            st.metric("Updated Balance", f"₹{result:,.2f}")
        else:
            st.error(result)


# ---------------- WITHDRAW MONEY ----------------

elif page == "Withdraw Money":

    st.title("💸 Withdraw Money")

    with st.form("withdraw_form"):

        account_no = st.text_input("Account Number")
        pin = st.text_input("4-digit PIN", type="password")

        amount = st.number_input(
            "Withdrawal Amount (₹)",
            min_value=0,
            value=100,
            step=100
        )

        submitted = st.form_submit_button(
            "Withdraw Money",
            type="primary"
        )

    if submitted:

        success, result = bank.withdraw_money(
            account_no, pin, int(amount)
        )

        if success:
            st.success("Withdrawal successful!")
            st.metric("Remaining Balance", f"₹{result:,.2f}")
        else:
            st.error(result)


# ---------------- CHECK BALANCE ----------------

elif page == "Check Balance":

    st.title("💳 Check Account Balance")

    with st.form("balance_form"):

        account_no = st.text_input("Account Number")
        pin = st.text_input("4-digit PIN", type="password")

        submitted = st.form_submit_button(
            "Check Balance",
            type="primary"
        )

    if submitted:

        success, result = bank.check_balance(
            account_no, pin
        )

        if success:
            st.success("Account verified!")
            st.metric("Available Balance", f"₹{result:,.2f}")
        else:
            st.error(result)


# ---------------- ACCOUNT DETAILS ----------------

elif page == "Account Details":

    st.title("📋 Account Details")

    with st.form("details_form"):

        account_no = st.text_input("Account Number")
        pin = st.text_input("4-digit PIN", type="password")

        submitted = st.form_submit_button(
            "View Account Details",
            type="primary"
        )

    if submitted:

        success, result = bank.get_account_details(
            account_no, pin
        )

        if success:
            st.success("Account verified!")

            col1, col2 = st.columns(2)

            col1.write("**Account Holder:**")
            col1.write(result["Name"])

            col1.write("**Age:**")
            col1.write(result["age"])

            col1.write("**Email:**")
            col1.write(result["email"])

            col2.write("**Account Number:**")
            col2.code(result["accountNo"])

            col2.metric(
                "Current Balance",
                f"₹{result['balance']:,.2f}"
            )

        else:
            st.error(result)


# ---------------- UPDATE DETAILS ----------------

elif page == "Update Details":

    st.title("⚙️ Update Account Details")

    with st.form("update_form"):

        account_no = st.text_input("Account Number")
        pin = st.text_input("Current 4-digit PIN", type="password")

        field = st.selectbox(
            "Select what you want to update",
            ["Name", "Email", "PIN"]
        )

        if field == "Name":
            new_value = st.text_input("New Name")

        elif field == "Email":
            new_value = st.text_input("New Email")

        else:
            new_value = st.text_input(
                "New 4-digit PIN",
                type="password",
                max_chars=4
            )

        submitted = st.form_submit_button(
            "Update Details",
            type="primary"
        )

    if submitted:

        success, result = bank.update_details(
            account_no, pin, field, new_value
        )

        if success:
            st.success(result)
        else:
            st.error(result)
