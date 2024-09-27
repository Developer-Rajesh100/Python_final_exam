import random

# User Class
class User:
    users = []

    def __init__(self, name, email, address, account_type, current_balance=0):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.current_balance = current_balance
        self.loan_amount = 0
        self.count_of_loans = 0
        self.account_number = None
        self.can_take_loan = True
        self.isBankrupt = False

    def create_account(self):
        account = CreateAccount(self.name, self.email, self.address, self.account_type)
        account_number_generator = AccountNumber()
        self.account_number = account_number_generator.generateNumber()
        User.users.append(self)
        print(f"Account created successfully. Your account number is {self.account_number}")

    def deposit(self, amount):
        self.current_balance += amount

    def withdraw(self, amount):
        if self.current_balance >= amount:
            self.current_balance -= amount
        else:
            return "Withdrawal amount exceeded"

    def check_balance(self):
        return self.current_balance

    def transaction_history(self):
        pass

    def is_eligible_for_loan(self):
        if self.count_of_loans < 2:
            return True
        else:
            return False

    def take_loan(self, amount):
        if self.is_eligible_for_loan() and self.can_take_loan:
            self.current_balance += amount
            self.loan_amount += amount
            self.count_of_loans += 1
            return f"Loan of {amount} granted. Your new balance is {self.current_balance}"
        else:
            return "You are not eligible for a loan"

    def transfer(self, amount, transfer_to):
        flag = False
        for user in User.users:
            if user.account_number == transfer_to:
                if self.current_balance >= amount:
                    self.current_balance -= amount
                    user.current_balance += amount
                    flag = True
                    return f"Transferred {amount} to account {transfer_to}. Your balance is now {self.current_balance}"
                else:
                    return "Insufficient balance"
        if not flag:
            return "Account does not exist"


class CreateAccount:
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type


class AccountNumber:
    def __init__(self):
        self.existing_numbers = set()

    def generateNumber(self):
        while True:
            account_number = random.randint(100000, 999999)
            if account_number not in self.existing_numbers:
                self.existing_numbers.add(account_number)
                return account_number

# Admin Class
class Admin:
    def __init__(self):
        pass

    def create_account(self, name, email, address, account_type):
        user = User(name, email, address, account_type)
        user.create_account()

    def delete_account(self, account_number):
        for user in User.users:
            if user.account_number == account_number:
                User.users.remove(user)
                return "Account deleted successfully"
        return "Account not found"

    def view_all_accounts(self):
        for user in User.users:
            print(f"Name: {user.name}, Email: {user.email}, Account Number: {user.account_number}")

    def total_balance(self):
        total = sum(user.current_balance for user in User.users)
        return total

    def total_loan(self):
        total = sum(user.loan_amount for user in User.users)
        return total

    def loan_off(self, account_number):
        for user in User.users:
            if user.account_number == account_number:
                user.can_take_loan = False
                return "Loan disabled for this account"

# Replica System
user = None

while True:
    print("\nWelcome to the bank")
    print("0. Admin Login")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check Balance")
    print("5. Transaction History")
    print("6. Take Loan")
    print("7. Transfer")
    print("8. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 0:
        print("""Admin Login Details:
        Username: admin
        Password: 1234""")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username == "admin" and password == "1234":
            admin = Admin()
            print("\nLogin successful")
            while True:
                print("0. Create Account")
                print("1. Delete Account")
                print("2. View All Accounts")
                print("3. Total Balance")
                print("4. Total Loan")
                print("5. Disable Loan for Account")
                print("6. Exit")

                admin_choice = int(input("Enter your choice: "))

                if admin_choice == 0:
                    name = input("Enter your name: ")
                    email = input("Enter your email: ")
                    address = input("Enter your address: ")
                    account_type = input("Enter your account type: ")
                    admin.create_account(name, email, address, account_type)

                elif admin_choice == 1:
                    account_number = int(input("Enter the account number to delete: "))
                    print(admin.delete_account(account_number))

                elif admin_choice == 2:
                    admin.view_all_accounts()

                elif admin_choice == 3:
                    print(f"Total balance: {admin.total_balance()}")

                elif admin_choice == 4:
                    print(f"Total loan: {admin.total_loan()}")

                elif admin_choice == 5:
                    account_number = int(input("Enter account number to disable loan: "))
                    print(admin.loan_off(account_number))

                elif admin_choice == 6:
                    break

        else:
            print("Invalid login credentials")

    elif choice == 1:
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        address = input("Enter your address: ")
        account_type = input("Enter your account type: ")
        user = User(name, email, address, account_type)
        user.create_account()

    elif choice == 2:
        if user is not None:
            amount = int(input("Enter the amount to deposit: "))
            user.deposit(amount)
            print("Amount deposited successfully")
        else:
            print("No user account found. Please create an account first.")

    elif choice == 3:
        if user is not None:
            amount = int(input("Enter the amount to withdraw: "))
            print(user.withdraw(amount))
        else:
            print("No user account found. Please create an account first.")

    elif choice == 4:
        if user is not None:
            print(f"Your current balance is {user.check_balance()}")
        else:
            print("No user account found. Please create an account first.")

    elif choice == 5:
        if user is not None:
            user.transaction_history()
        else:
            print("No user account found. Please create an account first.")

    elif choice == 6:
        if user is not None:
            amount = int(input("Enter the amount to take as loan: "))
            print(user.take_loan(amount))
        else:
            print("No user account found. Please create an account first.")

    elif choice == 7:
        if user is not None:
            amount = int(input("Enter the amount to transfer: "))
            transfer_to = int(input("Enter the account number to transfer to: "))
            print(user.transfer(amount, transfer_to))
        else:
            print("No user account found. Please create an account first.")

    elif choice == 8:
        break

    else:
        print("Invalid choice")
