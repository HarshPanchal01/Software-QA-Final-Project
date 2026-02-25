"""
CSCI 3060U - Software Quality Assurance
Phase 2: Front End Rapid Prototyping

Program Intention:
    This program acts as the Front End (ATM) for the Banking System. 
    It reads a valid bank accounts file, accepts user transactions via a CLI loop, 
    validates them against session limits and business rules, and (optionally) 
    outputs a transaction file at the end of the session.

Input Files:
    - bank_accounts.txt: Contains the current valid bank accounts.
    
Output Files:
    - bank_account_transaction_file.txt: Contains the log of all transactions 
      performed in the session.

Usage:
    Run the program using the command `qabank` (after installation) 
    or via `python3 -m src.front_end.cli`.
"""

from src.front_end.session import Session
from src.front_end.repository import AccountRepository
from src.front_end.models import MessageType, AccountStatus, AccountPlan, SessionType
from src.front_end.transactions import (
    Withdrawal, Transfer, Paybill, Deposit, Create, Delete, Disable, ChangePlan, EndOfSession
)

class ATMFrontEnd:
    """
    Handles direct interaction between the user and the system, valid and invalid commands,
    and writing the transaction file at the end of a session.
    
    Attributes:
        session: the current session object tracking front-end system state
        account_repository: runtime accounts loaded from a file
        transaction_list: list of transactions recorded from the current session.
    """
    
    ACCOUNTS_FILE = "bank_accounts.txt" # path to bank accounts file, used to load accounts to a repository
    
    # all transactions/commands that can be used in the system
    COMMANDS = {
        "login", "logout", "withdrawal", "transfer", "paybill",
        "deposit", "create", "delete", "disable", "changeplan", "help", "quit"
    }
    
    PRIVELEGED_COMMANDS = {"create", "delete", "disable", "changeplan"} # admin only commands
    
    def __init__(self, accounts_file: str = "bank_accounts.txt", transaction_file: str = "bank_account_transaction_file.txt"):
        self.session = Session()
        self.account_repository = AccountRepository()
        self.transaction_list = []
        self.accounts_file = accounts_file
        self.transaction_file = transaction_file
            
    def start(self) -> None:
        """
        Starts the ATM session loop.
        
        Intention:
            Continuously reads commands from standard input and processes them until
            the end of the input stream (EOF) is reached. If a user is logged in
            when EOF occurs, it automatically logs them out to ensure the transaction
            file is written.
        """
        self._print_message("Welcome to the QA Bank System (qabank)", MessageType.ACTION)
        self._print_message("Type 'login' to begin session.", MessageType.INFO)
        
        while True:
            try:
                command = self._read_line()
            except EOFError:
                # if end of input stream, force a logout. This will also write the transaction file.
                if self.session.is_logged_in():
                    self._handle_logout()
                break
            
            if command is None:
                continue
            
            self.process_command(command)
               
    """
    
        ATMFrontEnd Helper Methods
        
    """
            
    def _read_line(self) -> str | None:
        """
        Reads a single line of input from the user.
        
        Intention:
            Captures user input from stdin, strips leading/trailing whitespace.
            
        Returns:
            str | None: The cleaned command string, or None if the line was empty.
            
        Raises:
            EOFError: If the input stream is closed.
        """
        try:
            line = input()
        except EOFError:
            raise
            
        line = line.strip()
        if not line:
            return None
        return line
    
    def process_command(self, command) -> None:
        """
        Routes a user command to the appropriate handler.
        
        Intention:
            Acts as the central controller for the front end. It validates that:
            1. The command exists.
            2. The user is logged in (except for the 'login' command).
            3. The user has the required privileges (Admin vs Standard) for the command.
            If valid, it dispatches execution to the specific _handle_* method.
        
        Arguments:
            command (str): The raw command string entered by the user.
        """
        command = command.lower()
        
        # ignore command if it doesn't exist
        if command not in self.COMMANDS:
            self._print_message("Invalid Input. Please Enter Again.", MessageType.ERROR)
            return

        # Handle login if not already logged in
        if command == "login":
            if self.session.is_logged_in():
                self._print_message("You are already logged in. You must logout to login again.", MessageType.WARNING)
            else:
                self._handle_login()
            return
        
        if command == "help":
            self._handle_help()
            return

        if command == "quit":
            if self.session.is_logged_in():
                self.session.logout() # Ensure we log out to write transaction file if user tries to quit without logging out
            
            self._print_message("Exiting QA Bank System.", MessageType.ACTION)
            exit(0)
            return
        
        # If not logged in and user hasn't attempted to login, ignore
        if not self.session.is_logged_in():
            self._print_message("Error: Please login first.", MessageType.ERROR)
            return
        
        # ignore a privilege command request for a non-admin
        if command in self.PRIVELEGED_COMMANDS and not self.session.is_admin():
            self._print_message(f"Error: '{command}' is an admin-only command.", MessageType.ERROR)
            return
        
        match command:
            case "logout":
                self._handle_logout()
            case "withdrawal":
                self._handle_withdrawal()
            case "transfer":
                self._handle_transfer()
            case "paybill":
                self._handle_paybill()
            case "deposit":
                self._handle_deposit()
            case "create":
                self._handle_create()
            case "delete":
                self._handle_delete()
            case "disable":
                self._handle_disable()
            case "changeplan":
                self._handle_changeplan()
            
    def _handle_help(self) -> None:
        """
        Displays available commands based on session state.
        """
        visible_commands = set(self.COMMANDS)
        
        # if not logged in, only show login and quit commands.
        if not self.session.is_logged_in():
            visible_commands.intersection_update({"login", "quit"})
        
        # if logged in, dont show login command in help since it can't be used until logout.
        if self.session.is_logged_in():
            visible_commands.difference_update({"login"})

        # if session is not in admin, dont show admin only commands
        if not self.session.is_admin():
            visible_commands.difference_update(self.PRIVELEGED_COMMANDS)

        self._print_message(f"Available commands: {', '.join(visible_commands)}", MessageType.INFO)
    
    def _print_message(self, message, message_type: MessageType = MessageType.NORMAL) -> None:
        """
        Helper method to print a message to the console
        """
        override_color = False # Set to true to disable color for all messages.
        colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "cyan": "\033[36m",
        "gray": "\033[90m",
        "white": "\033[37m"
        }
        reset = "\033[0m"
        
        color_name = message_type.value if isinstance(message_type, MessageType) else None
        color_code = colors.get(color_name, "")
        
        if color_code and not override_color:
            print(f"{color_code}{message}{reset}")
        else:
            print(f"{message}")
    
    def _write_transaction_file(self) -> None:
        """
        Writes the daily transaction file.
        
        Intention:
            - Appends the mandatory 'End of Session' transaction (Code 00).
            - Iterates through self.transaction_list.
            - Writes each transaction's formatted string to the output file.
        """
        # Add End of Session transaction
        self.transaction_list.append(EndOfSession(self.session.current_user))
        
        try:
            with open(self.transaction_file, "w") as f:
                print("Daily Transaction File Content:")
                for t in self.transaction_list:
                    line = t.to_file_record()
                    if line:
                        f.write(line + "\n")
                        print(line)
        except IOError as e:
            self._print_message(f"Error writing transaction file: {e}", MessageType.ERROR)
            
    
    """
    
        ATMFrontEnd Transaction Handler Methods
        
    """
    
    
    def _handle_withdrawal(self) -> None:
        """
        Handles the 'withdrawal' transaction.
        Transaction code: 01
        
        Intention:
            - Prompts for account holder name (if Admin), account number, and amount.
            - Validates:
                1. Account exists.
                2. Account holder name matches (ownership).
                3. Standard session limit ($500) is not exceeded.
                4. Account has sufficient funds.
            - Records the valid transaction.
        """
        # 1. Account Holder Name
        holder_name = self.session.current_user
        if self.session.is_admin():
            self._print_message("Enter account holder name:", MessageType.INFO)
            holder_name = self._read_line()
            
        # 2. Account Number
        self._print_message("Enter account number:", MessageType.INFO)
        account_number = self._read_line()
        
        # 3. Amount
        self._print_message("Enter amount to withdraw:", MessageType.INFO)
        try:
            amount_str = self._read_line()
            if amount_str is None:
                self._print_message("Error: Amount cannot be empty.", MessageType.ERROR)
                return
            amount = float(amount_str)
        except ValueError:
            self._print_message("Error: Invalid amount format.", MessageType.ERROR)
            return

        # --- Validation ---
        
        # Check if account exists
        account = self.account_repository.find_account(account_number)
        if account is None:
            self._print_message("Error: Account not found.", MessageType.ERROR)
            return
            
        # Check ownership
        # "Bank account must be a valid account for the account holder currently logged in."
        if account.holder_name != holder_name:
            self._print_message("Error: Account holder name does not match.", MessageType.ERROR)
            return
            
        if not account.is_active():
            self._print_message("Error: Account is disabled.", MessageType.ERROR)
            return

        # Check session limit (Standard only)
        if not self.session.is_admin():
            if self.session.withdrawn_amount + amount > 500.00:
                self._print_message("Error: Session withdrawal limit ($500) exceeded.", MessageType.ERROR)
                return
                
        # Check balance
        # "Account balance must be at least $0.00 after withdrawal"
        # Note: We use the snapshot balance loaded at start of session.
        if account.balance - amount < 0.00:
            self._print_message("Error: Insufficient funds.", MessageType.ERROR)
            return

        # --- Execution ---
        
        # Create transaction
        transaction = Withdrawal(holder_name, account_number, amount)
        self.transaction_list.append(transaction)
        
        # Update session totals (Standard only)
        if not self.session.is_admin():
            self.session.withdrawn_amount += amount
            
        # Update in-memory balance to enforce constraints within the session
        account.balance -= amount
            
        self._print_message(f"Withdrawal of ${amount:.2f} successful.", MessageType.SUCCESS)
    

    def _handle_transfer(self) -> None:
        """
        Handles the front end logic for a 'transfer' transaction.
        Transaction code: 02

        Intention:
            - Prompts user for source account holder name, source account number,
                destination account number, and amount to transfer.
            - Validates:
                1. Source account exists and ownership matches.
                2. Destination account exists.
                3. Standard session transfer limit ($1000) is not exceeded.
                4. Both accounts have at least $0.00 balance after the transaction.
        """
        # 1. Account Holder Name
        holder_name = self.session.current_user
        if self.session.is_admin():
            self._print_message("Enter source account holder name:", MessageType.INFO)
            holder_name = self._read_line()

        # 2. Source Account Number
        self._print_message("Enter source account number:", MessageType.INFO)
        from_account_number = self._read_line()

        # 3. Destination Account Number
        self._print_message("Enter destination account number:", MessageType.INFO)
        to_account_number = self._read_line()

        # 4. Amount
        self._print_message("Enter amount to transfer:", MessageType.INFO)
        try:
            amount_str = self._read_line()
            if amount_str is None:
                self._print_message("Error: Amount cannot be empty.", MessageType.ERROR)
                return
            amount = float(amount_str)
        except ValueError:
            self._print_message("Error: Invalid amount format.", MessageType.ERROR)
            return

        # Validation 
        # validate source account exists
        from_account = self.account_repository.find_account(from_account_number)
        if from_account is None:
            self._print_message("Error: Source account not found.", MessageType.ERROR)
            return
        # validate source account name matches given source account name
        if from_account.holder_name != holder_name:
            self._print_message(f"Error: Account number {from_account_number} does not belong to holder {holder_name}.", MessageType.ERROR)
            return
            
        if not from_account.is_active():
            self._print_message("Error: Source account is disabled.", MessageType.ERROR)
            return

        # validate destination account exists 
        to_account = self.account_repository.find_account(to_account_number)
        if to_account is None:
            self._print_message("Error: Destination account not found.", MessageType.ERROR)
            return
            
        if not to_account.is_active():
            self._print_message("Error: Destination account is disabled.", MessageType.ERROR)
            return

        # validate session transfer limit (Standard only)
        if not self.session.is_admin():
            if self.session.transferred_amount + amount > 1000.00:
                self._print_message("Error: Session transfer limit ($1000) exceeded. Login as admin to bypass this limit.", MessageType.ERROR)
                return
        
        # validate source and destination accounts have at least $0.00 after transaction
        if from_account.balance - amount < 0.00:
            self._print_message("Error: Insufficient funds in source account.", MessageType.ERROR)
            return
        if to_account.balance + amount < 0.00:
            self._print_message("Error: Destination account would have negative balance.", MessageType.ERROR)
            return

        # Transaction
        transaction = Transfer(holder_name, from_account_number, to_account_number, amount)
        self.transaction_list.append(transaction)

        if not self.session.is_admin():
            self.session.transferred_amount += amount
            
        # Update in-memory balance
        from_account.balance -= amount

        self._print_message(f"Transfer of ${amount:.2f} successful.", MessageType.SUCCESS)
    
    def _handle_paybill(self) -> None:
        """
        Handles the 'paybill' transaction.
        Transaction code: 03
        
        Intention:
            - Prompts for account holder name (if Admin), account number, company, and amount.
            - Validates:
                1. Account exists and name matches.
                2. Company is one of the valid options (EC, CQ, FI).
                3. Standard session limit ($2000) is not exceeded.
                4. Account has sufficient funds.
            - Records the valid transaction.
        """
        # 1. Account Holder Name
        holder_name = self.session.current_user
        if self.session.is_admin():
            self._print_message("Enter account holder name:", MessageType.INFO)
            holder_name = self._read_line()
            
        # 2. Account Number
        self._print_message("Enter account number:", MessageType.INFO)
        account_number = self._read_line()
        
        # 3. Company
        self._print_message("Enter company name (EC, CQ, FI):", MessageType.INFO)
        company = self._read_line()
        
        # 4. Amount
        self._print_message("Enter amount to pay:", MessageType.INFO)
        try:
            amount_str = self._read_line()
            amount = float(amount_str)
        except ValueError:
            self._print_message("Error: Invalid amount format.", MessageType.ERROR)
            return

        # --- Validation ---
        
        account = self.account_repository.find_account(account_number)
        if account is None:
            self._print_message("Error: Account not found.", MessageType.ERROR)
            return
            
        if account.holder_name != holder_name:
            self._print_message("Error: Account holder name does not match.", MessageType.ERROR)
            return
            
        if not account.is_active():
            self._print_message("Error: Account is disabled.", MessageType.ERROR)
            return
            
        if company not in Paybill.COMPANIES:
            self._print_message("Error: Invalid company.", MessageType.ERROR)
            return

        # Check session limit (Standard only)
        if not self.session.is_admin():
            if self.session.paybill_amount + amount > 2000.00:
                self._print_message("Error: Session paybill limit ($2000) exceeded.", MessageType.ERROR)
                return
                
        # Check balance
        if account.balance - amount < 0.00:
            self._print_message("Error: Insufficient funds.", MessageType.ERROR)
            return

        # --- Execution ---
        
        transaction = Paybill(holder_name, account_number, company, amount)
        self.transaction_list.append(transaction)
        
        if not self.session.is_admin():
            self.session.paybill_amount += amount
            
        # Update in-memory balance
        account.balance -= amount
            
        self._print_message(f"bill of ${amount:.2f} to {company}: '{Paybill.COMPANIES[company]}' successful.", MessageType.SUCCESS)
        
    def _handle_deposit(self) -> None:
        """
        Handles the 'deposit' transaction.
        Transaction code: 04
        
        Intention:
            - Prompts for account holder name (if Admin), account number, and amount.
            - Validates:
                1. Account exists.
                2. Account holder name matches.
            - Records the valid transaction.
        """
        # 1. Account Holder Name
        holder_name = self.session.current_user
        if self.session.is_admin():
            self._print_message("Enter account holder name:", MessageType.INFO)
            holder_name = self._read_line()
            
        # 2. Account Number
        self._print_message("Enter account number:", MessageType.INFO)
        account_number = self._read_line()
        
        # 3. Amount
        self._print_message("Enter amount to deposit:", MessageType.INFO)
        try:
            amount_str = self._read_line()
            amount = float(amount_str)
        except ValueError:
            self._print_message("Error: Invalid amount format.", MessageType.ERROR)
            return

        # --- Validation ---
        
        account = self.account_repository.find_account(account_number)
        if account is None:
            self._print_message("Error: Account not found.", MessageType.ERROR)
            return
            
        if account.holder_name != holder_name:
            self._print_message(f"Error: Account holder name '{holder_name}' does not match '{account.holder_name}'.", MessageType.ERROR)
            return
            
        if not account.is_active():
            self._print_message("Error: Account is disabled.", MessageType.ERROR)
            return

        # --- Execution ---
        
        transaction = Deposit(holder_name, account_number, amount)
        self.transaction_list.append(transaction)
        self._print_message(f"Deposit of ${amount:.2f} successful.", MessageType.SUCCESS)

    def _handle_create(self) -> None:
        """
        Handles the 'create' transaction.
        Transaction code: 05

        Intention:
            - Prompts for account holder name and initial balance.
            - Validates:
                1. Account holder name is non-empty and at most 20 characters.
                2. Initial balance is a valid amount within transaction field limits.
        """
        self._print_message("Enter account holder name:", MessageType.INFO)
        holder_name = self._read_line()
        if not holder_name:
            self._print_message("Error: Name cannot be empty.", MessageType.ERROR)
            return
        if len(holder_name) > 20:
            self._print_message("Error: Account holder name cannot exceed 20 characters.", MessageType.ERROR)
            return

        self._print_message("Enter initial balance:", MessageType.INFO)
        try:
            initial_balance = float(self._read_line())
        except (TypeError, ValueError):
            self._print_message("Error: Invalid balance format.", MessageType.ERROR)
            return

        if initial_balance < 0.00:
            self._print_message("Error: Initial balance cannot be negative.", MessageType.ERROR)
            return
        if initial_balance > 99999.99:
            self._print_message("Error: Initial balance exceeds maximum allowed value ($99999.99).", MessageType.ERROR)
            return

        # Transaction
        transaction = Create(holder_name, initial_balance)
        self.transaction_list.append(transaction)
        self._print_message(f"Account of holder '{holder_name}' with ${initial_balance:.2f} has been created.", MessageType.SUCCESS)

    def _handle_delete(self) -> None: 
        """
        Handles the 'delete' transaction to delete an account.
        Transaction code: 06

        Intention:
            - Prompts for account holder name and account number.
            - Validates:
                1. Account matches the given account holder name and account number.
        """
        self._print_message("Enter account holder name:", MessageType.INFO)
        holder_name = self._read_line()

        self._print_message("Enter account number:", MessageType.INFO)
        account_number = self._read_line()

        # Validate account exists and matches given holder name
        account = self.account_repository.find_account(account_number)
        if account is None:
            self._print_message("Error: Account not found.", MessageType.ERROR)
            return
        if holder_name is None or holder_name.strip() == "":
            self._print_message("Error: Account holder name cannot be empty.", MessageType.ERROR)
            return
        if account.holder_name != holder_name:
            self._print_message(f"Error: Account number {account_number} does not belong to holder {holder_name}.", MessageType.ERROR)
            return

        # Transaction
        transaction = Delete(holder_name, account_number)
        self.transaction_list.append(transaction)
        
        # Update in-memory state
        self.account_repository.delete(account_number)
        
        self._print_message(f"Account {account_number} belonging to holder '{holder_name}' has been deleted.", MessageType.SUCCESS)

    def _handle_disable(self) -> None: 
        """
        Handles the 'disable' transaction to disable an account.
        Transaction code: 07

        Intention:
            - Prompts for account holder name and account number.
            - Changes the account status to 'Disabled' in the transaction file.
            - Validates:
                1. Account matches the given account holder name and account number.
                2. Session is Admin.
        """
        self._print_message("Enter account holder name:", MessageType.INFO)
        holder_name = self._read_line()

        self._print_message("Enter account number:", MessageType.INFO)
        account_number = self._read_line()

        # Validate account exists and matches given holder name
        account = self.account_repository.find_account(account_number)
        if account is None:
            self._print_message("Error: Account not found.", MessageType.ERROR)
            return
        if holder_name is None or holder_name.strip() == "":
            self._print_message("Error: Account holder name cannot be empty.", MessageType.ERROR)
            return
        if account.holder_name != holder_name:
            self._print_message(f"Error: Account number {account_number} does not belong to holder {holder_name}.", MessageType.ERROR)
            return
        
        # Transaction
        transaction = Disable(holder_name, account_number)
        self.transaction_list.append(transaction)
        
        # Update in-memory state
        account.status = AccountStatus.DISABLED
        
        self._print_message(f"Account {account_number} has been disabled.", MessageType.SUCCESS)
        
    def _handle_changeplan(self) -> None: 
        """
        Handles the 'changeplan' transaction to change an account's plan.
        Transaction code: 08

        Intention:
            - Prompts for account holder name and account number.
            - Changes the account plan from student (SP) to non-student (NP).
            - Validates:
                1. Account matches the given account holder name and account number.
                2. Session is Admin.
        """
        self._print_message("Enter account holder name:", MessageType.INFO)
        holder_name = self._read_line()

        self._print_message("Enter account number:", MessageType.INFO)
        account_number = self._read_line()

        # Validate account exists and matches given holder name
        account = self.account_repository.find_account(account_number)
        if account is None:
            self._print_message("Error: Account not found.", MessageType.ERROR)
            return
        if holder_name is None or holder_name.strip() == "":
            self._print_message("Error: Account holder name cannot be empty.", MessageType.ERROR)
            return
        if account.holder_name != holder_name:
            self._print_message(f"Error: Account number {account_number} does not belong to holder {holder_name}.", MessageType.ERROR)
            return

        # Transaction
        transaction = ChangePlan(holder_name, account_number)
        self.transaction_list.append(transaction)
        
        account.plan = AccountPlan.NON_STUDENT
        
        self._print_message(f"Account {account_number} plan has been changed.", MessageType.SUCCESS)
            
    def _handle_login(self) -> None:
        """
        Handles the 'login' transaction.
        Transaction code: N/A
        
        Intention:
            - Prompts user for session type (Standard/Admin).
            - If Standard, prompts for Account Holder Name.
            - Loads the current valid bank accounts from 'bank_accounts.txt' into memory.
            - Initializes the Session object.
        """
        if self.session.is_logged_in():
            self._print_message("Error: Already logged in.", MessageType.ERROR)
            return

        session_input = ""
        while True:
            self._print_message("Enter session type (standard/admin):", MessageType.INFO)
            session_input = self._read_line()
            
            if session_input in ["standard", "admin"]:
                break
            
            self._print_message("Error: Invalid session type.", MessageType.ERROR)
            
        name = ""
        if session_input == "standard":
            self._print_message("Enter account holder name:", MessageType.INFO)
            name = self._read_line()
            if not name:
                self._print_message("Error: Name cannot be empty.", MessageType.ERROR)
                return

        # Load accounts (Requirement: reads in current bank accounts file)
        self.account_repository.load_from_file(self.accounts_file)
        
        stype = SessionType.ADMIN if session_input == "admin" else SessionType.STANDARD
        self.session.login(stype, name)
        
        login_msg = f"Successfully logged in as an admin." if self.session.is_admin() else f"Successfully logged in as '{name}'."
        
        self._print_message(login_msg, MessageType.SUCCESS)
    
    def _handle_logout(self) -> None:
        """
        Handles the 'logout' transaction.
        Transaction code: N/A
        
        Intention:
            - Writes all accumulated transactions from the session to 'bank_account_transaction_file.txt'.
            - Clears the transaction history.
            - Resets the session state (logs out).
        """
        if not self.session.is_logged_in():
            self._print_message("Error: Not logged in.", MessageType.ERROR)
            return

        self._write_transaction_file()
        self.session.logout()
        self.transaction_list.clear() # Clear transactions for next session
        self._print_message("Successfully logged out.", MessageType.SUCCESS)

import sys

def main():
    """
    Entry point for the Banking System Front End.
    """
    accounts_file = "bank_accounts.txt"
    transaction_file = "bank_account_transaction_file.txt"
    
    if len(sys.argv) >= 3:
        accounts_file = sys.argv[1]
        transaction_file = sys.argv[2]
        
    app = ATMFrontEnd(accounts_file, transaction_file)
    app.start()

if __name__ == "__main__":
    main()
