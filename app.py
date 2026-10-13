
import streamlit as st
from main import bank

st.set_page_config(
    page_title="MyBank | Banking Dashboard",
    page_icon="🏦",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("🏦 MyBank")
st.sidebar.caption("Bank Management System")

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

# Dashboard
if page == "Dashboard":

    st.title("Welcome to MyBank 👋")
    st.write("It's a simple banking management dashboard.")

    total_accounts = len(bank.data)
    total_balance = sum(
        account["balance"] for account in bank.data
    )

    col1, col2 = st.columns(2)

    col1.metric("Total Accounts", total_accounts)
    col2.metric("Total Account Balances", f"₹{total_balance:,.2f}")

    st.divider()

    st.subheader("Available Services")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(" Create a new account")

    with col2:
        st.info(" Deposit or withdraw money")

    with col3:
        st.info(" View and update account details")

   


elif page == "Create Account":

    import random
    import string

    st.title("👤 Create a New Account")
    st.write("Fill in your details to get started.")

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

        if not name.strip() or not email.strip():
            st.error("Please enter your name and email.")

        elif age < 18:
            st.error("You must be at least 18 years old.")

        elif not pin.isdigit() or len(pin) != 4:
            st.error("PIN must contain exactly 4 digits.")

        else:
            # Generate an account number
            while True:
                characters = (
                    random.choices(string.ascii_letters, k=5)
                    + random.choices(string.digits, k=5)
                )

                random.shuffle(characters)
                account_no = "".join(characters)

                if not any(
                    account["accountNo"] == account_no
                    for account in bank.data
                ):
                    break

            # Use the same data structure as your backend
            info = {
                "Name": name.strip(),
                "age": int(age),
                "email": email.strip(),
                "pin": int(pin),
                "accountNo": account_no,
                "balance": 0
            }

            bank.data.append(info)
            bank.update()

            st.success("Account created successfully!")

            st.write("Your account number:")
            st.code(account_no)

            st.warning(
                "Save this account number. "
                "Your opening balance is ₹0."
            )
        
elif page == "Deposit Money":

    st.title("💰 Deposit Money")
    st.write("Add money to your bank account.")

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

        if not account_no.strip():
            st.error("Please enter your account number.")

        elif not pin.isdigit() or len(pin) != 4:
            st.error("Please enter a valid 4-digit PIN.")

        else:
            userdata = [
                account for account in bank.data
                if account["accountNo"] == account_no.strip()
                and account["pin"] == int(pin)
            ]

            if not userdata:
                st.error("Invalid account number or PIN.")

            elif amount <= 0:
                st.error("Deposit amount must be greater than zero.")

            else:
                userdata[0]["balance"] += amount
                bank.update()

                st.success(
                    f"₹{amount:,.2f} deposited successfully!"
                )

                st.metric(
                    "Updated Balance",
                    f"₹{userdata[0]['balance']:,.2f}"
                )
            
elif page == "Withdraw Money":

    st.title("💸 Withdraw Money")
    st.write("Withdraw money from your bank account.")

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

        if not account_no.strip():
            st.error("Please enter your account number.")

        elif not pin.isdigit() or len(pin) != 4:
            st.error("Please enter a valid 4-digit PIN.")

        else:
            userdata = [
                account for account in bank.data
                if account["accountNo"] == account_no.strip()
                and account["pin"] == int(pin)
            ]

            if not userdata:
                st.error("Invalid account number or PIN.")

            elif amount <= 0:
                st.error("Withdrawal amount must be greater than zero.")

            elif amount > userdata[0]["balance"]:
                st.error("Insufficient account balance.")

            else:
                userdata[0]["balance"] -= amount
                bank.update()

                st.success(
                    f"₹{amount:,.2f} withdrawn successfully!"
                )

                st.metric(
                    "Remaining Balance",
                    f"₹{userdata[0]['balance']:,.2f}"
                )

elif page == "Check Balance":

    st.title("💳 Check Account Balance")
    st.write("Securely check your current account balance.")

    with st.form("balance_form"):

        account_no = st.text_input("Account Number")
        pin = st.text_input("4-digit PIN", type="password")

        submitted = st.form_submit_button(
            "Check Balance",
            type="primary"
        )

    if submitted:

        if not account_no.strip():
            st.error("Please enter your account number.")

        elif not pin.isdigit() or len(pin) != 4:
            st.error("Please enter a valid 4-digit PIN.")

        else:
            userdata = [
                account for account in bank.data
                if account["accountNo"] == account_no.strip()
                and account["pin"] == int(pin)
            ]

            if not userdata:
                st.error("Invalid account number or PIN.")

            else:
                account = userdata[0]

                st.success("Account verified successfully!")

                st.metric(
                    "Available Balance",
                    f"₹{account['balance']:,.2f}"
                )

elif page == "Account Details":

    st.title("📋 Account Details")
    st.write("View your account information securely.")

    with st.form("details_form"):

        account_no = st.text_input("Account Number")
        pin = st.text_input("4-digit PIN", type="password")

        submitted = st.form_submit_button(
            "View Account Details",
            type="primary"
        )

    if submitted:

        if not account_no.strip():
            st.error("Please enter your account number.")

        elif not pin.isdigit() or len(pin) != 4:
            st.error("Please enter a valid 4-digit PIN.")

        else:
            userdata = [
                account for account in bank.data
                if account["accountNo"] == account_no.strip()
                and account["pin"] == int(pin)
            ]

            if not userdata:
                st.error("Invalid account number or PIN.")

            else:
                account = userdata[0]

                st.success("Account verified successfully!")

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Account Holder**")
                    st.write(account["Name"])

                    st.write("**Age**")
                    st.write(account["age"])

                    st.write("**Email Address**")
                    st.write(account["email"])

                with col2:
                    st.write("**Account Number**")
                    st.code(account["accountNo"])

                    st.write("**Account Balance**")
                    st.metric(
                        "Available Balance",
                        f"₹{account['balance']:,.2f}"
                    )

elif page == "Update Details":

    st.title("⚙️ Update Account Details")
    st.write("Change your account information securely.")

    with st.form("update_details_form"):

        account_no = st.text_input("Account Number")
        pin = st.text_input("Current 4-digit PIN", type="password")

        field = st.selectbox(
            "Select information to update",
            ["Name", "Email", "PIN"]
        )

        if field == "Name":
            new_value = st.text_input("New Name")

        elif field == "Email":
            new_value = st.text_input("New Email Address")

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

        if not account_no.strip():
            st.error("Please enter your account number.")

        elif not pin.isdigit() or len(pin) != 4:
            st.error("Please enter your current 4-digit PIN.")

        else:
            userdata = [
                account for account in bank.data
                if account["accountNo"] == account_no.strip()
                and account["pin"] == int(pin)
            ]

            if not userdata:
                st.error("Invalid account number or current PIN.")

            elif field in ["Name", "Email"] and not new_value.strip():
                st.error(f"{field} cannot be empty.")

            elif field == "PIN" and (
                not new_value.isdigit() or len(new_value) != 4
            ):
                st.error("The new PIN must contain exactly 4 digits.")

            else:
                account = userdata[0]

                if field == "Name":
                    account["Name"] = new_value.strip()

                elif field == "Email":
                    account["email"] = new_value.strip()

                else:
                    account["pin"] = int(new_value)

                bank.update()

                st.success(f"{field} updated successfully!")
                st.info("Your changes have been saved.")
