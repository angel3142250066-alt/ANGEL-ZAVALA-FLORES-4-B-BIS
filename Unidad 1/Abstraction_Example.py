class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"${amount} deposited successfully.")
        else:
            print("Invalid amount.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"${amount} withdrawn successfully.")
        else:
            print("Invalid amount or insufficient balance.")

    def show_balance(self):
        print(f"Owner: {self.owner}")
        print(f"Current balance: ${self.balance}")


# Create an account
account = BankAccount("Angel", 1000)

# Show initial balance
account.show_balance()

# Deposit money
account.deposit(500)

# Withdraw money
account.withdraw(300)

# Show final balance
account.show_balance()