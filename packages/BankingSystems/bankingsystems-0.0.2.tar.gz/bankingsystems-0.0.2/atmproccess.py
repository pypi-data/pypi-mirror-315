import tkinter as tk
from tkinter import messagebox

class BankAccount:
    def __init__(self):
        self.amount = 0  # Initializing the account balance to 0
        self.pin = "1234"  # Default PIN

    def deposit(self, amount):
        self.amount += amount  # Adds the amount deposited to the account balance
        return f"Amount Deposited Successfully. New Bank Balance: ${self.amount:.2f}"

    def withdraw_funds(self, amount):
        if amount <= 0:
            # Check for invalid withdrawal amount
            return "Error: Withdrawal amount must be greater than zero."
        elif amount > self.amount:
            return "Error: Insufficient funds."  # Check for sufficient balance
        else:
            self.amount -= amount  # Deduct withdrawal amount from the account balance
            # Return the balance after the withdrawal
            return f"Success: Withdrawn ${amount:.2f}. New balance: ${self.amount:.2f}"

    def show_balance(self):
        # Shows the current account balance
        return f"Your Balance Is: ${self.amount:.2f}"

    def transfer(self, destination_account, amount):
        if amount <= 0:
            return "Your transfer has to be more than 0."  # Check for valid transfer amount
        elif amount > self.amount:
            # Check for sufficient balance for transfer
            return "Sorry you have insufficient funds."
        else:
            self.amount -= amount  # Deduct the transfer amount from source account
            # Add the transfer amount to destination account
            destination_account.amount += amount
            return f"Yay: Your ${amount:.2f} has been transferred to its destination."
        
    def change_pin(self, current_pin, new_pin):
        if current_pin != self.pin: 
            return "Invalid old PIN, Please try again" 
        else: 
            self.pin = new_pin
            return "ATM Card PIN Is Updated!"
        
class BankApp:
    def __init__(self, root):
        self.root = root
        # Set the title of the application window
        self.root.title("Bank Account Manager")

        self.checking_account = BankAccount()  # Initialize checking account
        self.savings_account = BankAccount()  # Initialize savings account

        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        self.pin_label = tk.Label(self.login_frame, text="Enter PIN:")
        self.pin_label.pack()

        self.pin_entry = tk.Entry(self.login_frame, show="*")
        self.pin_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.verify_login)
        self.login_button.pack()

    def verify_login(self):
        entered_pin = self.pin_entry.get()
        if entered_pin == self.checking_account.pin or entered_pin == self.savings_account.pin:
            self.login_frame.pack_forget()
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Invalid PIN entered.")

    def create_main_screen(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        # Labels and Entry Fields
        # Label for selecting account
        self.account_label = tk.Label(self.main_frame, text="Choose Account:")
        self.account_label.pack()

        # Variable to store selected account type
        self.account_var = tk.StringVar(value="checking")
        self.checking_radio = tk.Radiobutton(
            # Radio button for checking account
            self.main_frame, text="Checking", variable=self.account_var, value="checking")
        self.checking_radio.pack()

        self.savings_radio = tk.Radiobutton(
            # Radio button for savings account
            self.main_frame, text="Savings", variable=self.account_var, value="savings")
        self.savings_radio.pack()

        # Label for entering amount
        self.amount_label = tk.Label(self.main_frame, text="Enter Amount:")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(self.main_frame)  # Entry field for amount
        self.amount_entry.pack()

        # Buttons
        self.deposit_button = tk.Button(
            self.main_frame, text="Deposit", command=self.deposit)  # Button to deposit
        self.deposit_button.pack()

        self.withdraw_button = tk.Button(
            self.main_frame, text="Withdraw", command=self.withdraw)  # Button to Withdraw
        self.withdraw_button.pack()

        self.balance_button = tk.Button(
            # Button to show account balance
            self.main_frame, text="Show Balance", command=self.show_balance)
        self.balance_button.pack()

        self.transfer_button = tk.Button(
            self.main_frame, text="Transfer", command=self.transfer)  # Balance to transfer
        self.transfer_button.pack()

        self.change_pin_button = tk.Button(
            self.main_frame, text="Change PIN", command=self.show_change_pin_screen)  # Button to change PIN
        self.change_pin_button.pack()

    def show_change_pin_screen(self):
        self.main_frame.pack_forget()
        self.change_pin_frame = tk.Frame(self.root)
        self.change_pin_frame.pack()

        # Entry fields for changing PIN
        self.current_pin_label = tk.Label(self.change_pin_frame, text="Current PIN:")
        self.current_pin_label.pack()
        self.current_pin_entry = tk.Entry(self.change_pin_frame, show="*")
        self.current_pin_entry.pack()

        self.new_pin_label = tk.Label(self.change_pin_frame, text="New PIN:")
        self.new_pin_label.pack()
        self.new_pin_entry = tk.Entry(self.change_pin_frame, show="*")
        self.new_pin_entry.pack()

        self.confirm_pin_button = tk.Button(
            self.change_pin_frame, text="Confirm", command=self.change_pin)
        self.confirm_pin_button.pack()

    def change_pin(self):
        account = self.get_selected_account()  # Get the selected account
        current_pin = self.current_pin_entry.get()
        new_pin = self.new_pin_entry.get()
        message = account.change_pin(current_pin, new_pin)  # Perform the PIN change operation
        # Display the result in a message box
        messagebox.showinfo("Change PIN", message)
        self.checking_account.pin = new_pin
        self.savings_account.pin = new_pin
        self.change_pin_frame.pack_forget()
        self.create_login_screen()

    def get_selected_account(self):
        # Return the selected account (checking or savings) based on the radio button selection
        return self.checking_account if self.account_var.get() == "checking" else self.savings_account

    def deposit(self):
        account = self.get_selected_account()  # Get the selected account
        try:
            # Get the deposit amount from entry field
            amount = float(self.amount_entry.get())
            message = account.deposit(amount)  # Perform deposit operation
            # Display the result in a message box
            messagebox.showinfo("Deposit", message)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered.")

    def withdraw(self):
        account = self.get_selected_account()  # Get the selected account
        try:
            # Get the withdraw amount from entry field
            amount = float(self.amount_entry.get())
            # Perform the withdraw operation
            message = account.withdraw_funds(amount)
            # Display the result in a message box
            messagebox.showinfo("Withdraw", message)
        except ValueError:
            # Handle invalid input
            messagebox.showerror("Error", "Invalid amount entered.")

    def show_balance(self):
        account = self.get_selected_account()  # Get the selected account
        message = account.show_balance()  # Get the current balance
        # Display the balance in a message box
        messagebox.showinfo("Balance", message)

    def transfer(self):
        account = self.get_selected_account()  # Get the selected account
        try:
            # Get the transfer amount from entry field
            amount = float(self.amount_entry.get())
            source_account = self.get_selected_account()  # Get the source account
            # Determine the destination account
            destination_account = self.savings_account if source_account == self.checking_account else self.checking_account
            # Perform the transfer operation
            message = source_account.transfer(destination_account, amount)
            # Display the result in a message box
            messagebox.showinfo("Transfer", message)
        except ValueError:
            # Handle invalid input
            messagebox.showerror("Error", "Invalid amount entered.")


if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    app = BankApp(root)  # Instantiate the BankApp
    root.mainloop()  # Run the Tkinter main event loop