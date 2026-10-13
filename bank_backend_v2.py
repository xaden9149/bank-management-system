
import json
import random
import string
from pathlib import Path


class Bank:

    database = "data.json"

    def __init__(self):
        if Path(self.database).exists():
            with open(self.database, "r") as file:
                self.data = json.load(file)
        else:
            self.data = []

    def update(self):
        with open(self.database, "w") as file:
            json.dump(self.data, file, indent=4)

    def generate_account_number(self):
        while True:
            letters = random.choices(string.ascii_letters, k=5)
            numbers = random.choices(string.digits, k=5)

            account_no = letters + numbers
            random.shuffle(account_no)
            account_no = "".join(account_no)

            # Check whether this number already exists
            found = False

            for account in self.data:
                if account["accountNo"] == account_no:
                    found = True
                    break

            if not found:
                return account_no

    def find_account(self, account_no, pin):
        for account in self.data:
            if (
                account["accountNo"] == account_no
                and account["pin"] == int(pin)
            ):
                return account

        return None

    def create_account(self, name, age, email, pin):

        if name == "" or email == "":
            return False, "Name and email cannot be empty."

        if age < 18:
            return False, "You must be at least 18 years old."

        if len(pin) != 4 or not pin.isdigit():
            return False, "PIN must contain 4 digits."

        account = {
            "Name": name,
            "age": age,
            "email": email,
            "pin": int(pin),
            "accountNo": self.generate_account_number(),
            "balance": 0
        }

        self.data.append(account)
        self.update()

        return True, account["accountNo"]

    def deposit_money(self, account_no, pin, amount):

        account = self.find_account(account_no, pin)

        if account is None:
            return False, "Invalid account number or PIN."

        if amount <= 0 or amount > 10000:
            return False, "Deposit must be between ₹1 and ₹10,000."

        account["balance"] += amount
        self.update()

        return True, account["balance"]

    def withdraw_money(self, account_no, pin, amount):

        account = self.find_account(account_no, pin)

        if account is None:
            return False, "Invalid account number or PIN."

        if amount <= 0:
            return False, "Amount must be greater than zero."

        if amount > account["balance"]:
            return False, "Insufficient balance."

        account["balance"] -= amount
        self.update()

        return True, account["balance"]

    def check_balance(self, account_no, pin):

        account = self.find_account(account_no, pin)

        if account is None:
            return False, "Invalid account number or PIN."

        return True, account["balance"]

    def get_account_details(self, account_no, pin):

        account = self.find_account(account_no, pin)

        if account is None:
            return False, "Invalid account number or PIN."

        details = {}

        for key in account:
            if key != "pin":
                details[key] = account[key]

        return True, details

    def update_details(self, account_no, pin, field, new_value):

        account = self.find_account(account_no, pin)

        if account is None:
            return False, "Invalid account number or PIN."

        if field == "Name":
            if new_value == "":
                return False, "Name cannot be empty."

            account["Name"] = new_value

        elif field == "Email":
            if new_value == "":
                return False, "Email cannot be empty."

            account["email"] = new_value

        elif field == "PIN":
            if len(new_value) != 4 or not new_value.isdigit():
                return False, "PIN must contain 4 digits."

            account["pin"] = int(new_value)

        else:
            return False, "Invalid field."

        self.update()

        return True, "Details updated successfully."
