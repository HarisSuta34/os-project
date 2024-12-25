import threading
import json
from account import Account

# Dictionary to store user accounts and passwords
user_accounts = {}
# Semaphore to limit concurrent access to one user
user_semaphore = threading.Semaphore(1)
# Admin username
ADMIN_USERNAME = "admin"
# JSON file to store user accounts
USER_ACCOUNTS_FILE = "user_accounts.json"

def load_user_accounts():
    global user_accounts
    try:
        with open(USER_ACCOUNTS_FILE, "r") as file:
            data = json.load(file)
            for username, (balance, password) in data.items():
                user_accounts[username] = (Account(balance), password)
    except FileNotFoundError:
        pass

def save_user_accounts():
    data = {username: (account.get_balance(), password) for username, (account, password) in user_accounts.items()}
    with open(USER_ACCOUNTS_FILE, "w") as file:
        json.dump(data, file)

def user_session(username):
    account = user_accounts[username][0]
    print(f"Welcome {username} to the Concurrent Transaction Processing System")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. View Balance")
    print("4. Logout")
    print("========================================")

    while True:
        choice = input("Enter your choice: ")
        if choice == '1':
            while True:
                amount = float(input("Enter amount to deposit: "))
                if amount <= 0:
                    print("Invalid amount. Please enter a positive amount.")
                    print("========================================")
                else:
                    break
            threading.Thread(target=account.deposit, args=(amount,)).start()
            save_user_accounts()  # Save accounts after deposit
            print("========================================")
        elif choice == '2':
            amount = float(input("Enter amount to withdraw: "))
            threading.Thread(target=account.withdraw, args=(amount,)).start()
            save_user_accounts()  # Save accounts after withdrawal
            print("========================================")
        elif choice == '3':
            print(f"Current balance: {account.get_balance()}")
            print("========================================")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")
            print("========================================")

def admin_session():
    print("Welcome admin to the Concurrent Transaction Processing System")
    print("1. List all user accounts")
    print("2. Delete a user account")
    print("3. Logout")
    print("========================================")

    while True:
        choice = input("Enter your choice: ")
        if choice == '1':
            if len(user_accounts) > 1:  # Check if there are other users
                for username, (account, _) in user_accounts.items():
                    if username != ADMIN_USERNAME:
                        print(f"User: {username}, Balance: {account.get_balance()}")
                print("========================================")
            else:
                print("No active users.")
                print("========================================")
        elif choice == '2':
            username_to_delete = input("Enter the username of the account to delete: ")
            if username_to_delete in user_accounts and username_to_delete != ADMIN_USERNAME:
                del user_accounts[username_to_delete]
                save_user_accounts()  # Save accounts after deletion
                print(f"Account for user '{username_to_delete}' has been deleted.")
                print("========================================")
            else:
                print("Account does not exist or cannot delete admin account.")
                print("========================================")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
            print("========================================")

def main():
    load_user_accounts()
    if ADMIN_USERNAME not in user_accounts:
        user_accounts[ADMIN_USERNAME] = (Account(0), "admin_password")  # Initialize admin account with balance 0
        save_user_accounts()
    while True:
        print("1. Login")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            while True:
                username = input("Enter your username: ")
                if not username or len(username) < 4 or username.isdigit() or not any(char.isalpha() for char in username):
                    print("Invalid username. Please enter a username that is at least 4 characters long, contains letters, and is not empty or only symbols.")
                    print("========================================")
                else:
                    break
            if username not in user_accounts:
                while True:
                    password = input("Enter a password for your new account: ")
                    if len(password) < 4:
                        print("Invalid password. Please enter a password that is at least 4 characters long.")
                        print("========================================")
                    else:
                        break
                user_accounts[username] = (Account(0), password)  # Create a new account with initial balance 0 and password
                save_user_accounts()  # Save accounts after creation
                print("Account created successfully.")
                print("========================================")
            password = input("Enter your password: ")
            if user_accounts[username][1] == password:
                if username == ADMIN_USERNAME:
                    if user_semaphore.acquire(blocking=False):
                        try:
                            admin_session()
                        finally:
                            user_semaphore.release()
                    else:
                        print("Another user is currently logged in. Please wait.")
                        print("========================================")
                else:
                    if user_semaphore.acquire(blocking=False):
                        try:
                            user_session(username)
                        finally:
                            user_semaphore.release()
                    else:
                        print("Another user is currently logged in. Please wait.")
                        print("========================================")
            else:
                print("Incorrect password. Please try again.")
                print("========================================")
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")
            print("========================================")

if __name__ == "__main__":
    main()