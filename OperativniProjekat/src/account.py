import threading

class Account:
    def __init__(self, balance=0):
        self.balance = balance
        self.lock = threading.Lock()

    def deposit(self, amount):
        with self.lock:
            self.balance += amount
            print(f"Deposited {amount}, new balance is {self.balance}")

    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                print(f"Withdrew {amount}, new balance is {self.balance}")
            else:
                print("Insufficient funds")

    def get_balance(self):
        with self.lock:
            return self.balance