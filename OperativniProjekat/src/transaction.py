class Transaction:
    def __init__(self, account):
        self.account = account

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.account.deposit(amount)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        self.account.withdraw(amount)