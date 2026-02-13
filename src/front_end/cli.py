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
from src.front_end.models import SessionType
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
    
    # path to the bank accounts file, this will be given to accounts_repository to load all bank accounts
    ACCOUNTS_FILE = "bank_accounts.txt"
    
    # all transaction commands that can be used in the system
    COMMANDS = {
        "login", "logout", "withdrawal", "transfer", "paybill",
        "deposit", "create", "delete", "disable", "changeplan", "help", "quit"
    }
    
    # all transaction commands that require admin privileges
    PRIVELEGED_COMMANDS = {"create", "delete", "disable", "changeplan"}
    
    
    def __init__(self):
        self.session = Session()
        self.account_repository = AccountRepository()
        self.transaction_list = []
    
    def start(self) -> None:
        """
        Starts the ATM session loop.
        
        Intention:
            Continuously reads commands from standard input and processes them until
            the end of the input stream (EOF) is reached. If a user is logged in
            when EOF occurs, it automatically logs them out to ensure the transaction
            file is written.
        """
        print("Welcome to the QA Bank System (qabank)")
        print("Type 'login' to begin session.")
        
        while True:
            try:
                command = self.read_line()
            except EOFError:
                # End of input stream, user has closed the terminal
                if self.session.is_logged_in():
                    self._handle_logout()
                break
            
            if command is None:
                continue
            
            self.process_command(command)
            
    def read_line(self) -> str | None:
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
            
        command = line.strip()
        if not command:
            return None
        return command
    
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
        command_lower = command.lower()
        
        # ignore command if it doesn't exist
        if command_lower not in self.COMMANDS:
            self._print_message(f"Error: command '{command}' does not exist. Type 'help' for a list of commands.")
            return

        # Handle login if not already logged in
        if command_lower == "login":
            if self.session.is_logged_in():
                self._print_message("Error: Already logged in.")
            else:
                self._handle_login()
            return
        
        if command_lower == "help":
            self._handle_help()
            return

        if command_lower == "quit":
            if self.session.is_logged_in():
                self._print_message("Error: Please logout first.")
            else:
                self._print_message("Exiting QA Bank System.")
                exit(0)
            return
        
        # If not logged in and user hasn't attempted to login, ignore
        if not self.session.is_logged_in():
            self._print_message("Error: Please login first.")
            return
        
        # ignore a privilege command request for a non-admin
        if command_lower in self.PRIVELEGED_COMMANDS and not self.session.is_admin():
            self._print_message(f"Error: '{command}' is an admin-only command.")
            return
        
        match command_lower:
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
            case "help":
                self._handle_help()
            
    def _handle_help(self):
        """
        Displays available commands based on session state.
        """
        if not self.session.is_logged_in():
            print("Available commands: login, quit")
            return
            
        cmds = ["logout", "withdrawal", "transfer", "paybill", "deposit"]
        if self.session.is_admin():
            cmds.extend(["create", "delete", "disable", "changeplan"])
            
        print(f"Available commands: {', '.join(cmds)}")

    def _handle_transfer(self): 
        # TODO (Nathan): Implement transfer logic (verify ownership, destination, $1000 limit)
        self._print_message("Feature 'transfer' not implemented yet.")

    def _handle_create(self): 
        # TODO (Nathan): Implement create logic (Admin only, unique number check)
        self._print_message("Feature 'create' not implemented yet.")

    def _handle_delete(self): 
        # TODO (Nathan): Implement delete logic (Admin only, name/number match)
        self._print_message("Feature 'delete' not implemented yet.")

    def _handle_disable(self): 
        # TODO (Nathan): Implement disable logic (Admin only)
        self._print_message("Feature 'disable' not implemented yet.")

    def _handle_changeplan(self): 
        # TODO (Nathan): Implement changeplan logic (Admin only, SP <-> NP)
        self._print_message("Feature 'changeplan' not implemented yet.")
            
    def _handle_login(self) -> None:
        """
        Handles the 'login' transaction.
        
        Intention:
            - Prompts user for session type (Standard/Admin).
            - If Standard, prompts for Account Holder Name.
            - Loads the current valid bank accounts from 'bank_accounts.txt' into memory.
            - Initializes the Session object.
        """
        if self.session.is_logged_in():
            self._print_message("Error: Already logged in.")
            return

        self._print_message("Enter session type (standard/admin):")
        session_input = self.read_line()
        
        if session_input not in ["standard", "admin"]:
            self._print_message("Error: Invalid session type.")
            return
            
        name = ""
        if session_input == "standard":
            self._print_message("Enter account holder name:")
            name = self.read_line()
            if not name:
                self._print_message("Error: Name cannot be empty.")
                return

        # Load accounts (Requirement: reads in current bank accounts file)
        self.account_repository.load_from_file(self.ACCOUNTS_FILE)
        
        stype = SessionType.ADMIN if session_input == "admin" else SessionType.STANDARD
        self.session.login(stype, name)
        
        login_msg = f"Successfully logged in as {session_input}"
        if name:
            login_msg += f" (User: {name})"
        login_msg += "."
        
        self._print_message(login_msg)
    
    def _handle_logout(self) -> None:
        """
        Handles the 'logout' transaction.
        
        Intention:
            - Writes all accumulated transactions from the session to 'bank_account_transaction_file.txt'.
            - Clears the transaction history.
            - Resets the session state (logs out).
        """
        if not self.session.is_logged_in():
            self._print_message("Error: Not logged in.")
            return

        self._write_transaction_file()
        self.session.logout()
        self.transaction_list.clear() # Clear transactions for next session
        self._print_message("Successfully logged out.")
        
    def _write_transaction_file(self) -> None:
        """
        Writes the daily transaction file.
        
        Intention:
            - Appends the mandatory 'End of Session' transaction (Code 00).
            - Iterates through self.transaction_list.
            - Writes each transaction's formatted string to the output file.
        """
        # Add End of Session transaction
        self.transaction_list.append(EndOfSession())
        
        output_filename = "bank_account_transaction_file.txt"
        try:
            with open(output_filename, "w") as f:
                for t in self.transaction_list:
                    line = t.to_file_record()
                    if line:
                        f.write(line + "\n")
        except IOError as e:
            self._print_message(f"Error writing transaction file: {e}")
    
    def _handle_withdrawal(self) -> None:
        """
        Handles the 'withdrawal' transaction.
        
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
            self._print_message("Enter account holder name:")
            holder_name = self.read_line()
            
        # 2. Account Number
        self._print_message("Enter account number:")
        account_number = self.read_line()
        
        # 3. Amount
        self._print_message("Enter amount to withdraw:")
        try:
            amount_str = self.read_line()
            amount = float(amount_str)
        except ValueError:
            self._print_message("Error: Invalid amount format.")
            return

        # --- Validation ---
        
        # Check if account exists
        account = self.account_repository.find_account(account_number)
        if account is None:
            self._print_message("Error: Account not found.")
            return
            
        # Check ownership
        # "Bank account must be a valid account for the account holder currently logged in."
        if account.holder_name != holder_name:
            self._print_message("Error: Account holder name does not match.")
            return

        # Check session limit (Standard only)
        if not self.session.is_admin():
            if self.session.withdrawn_amount + amount > 500.00:
                self._print_message("Error: Session withdrawal limit ($500) exceeded.")
                return
                
        # Check balance
        # "Account balance must be at least $0.00 after withdrawal"
        # Note: We use the snapshot balance loaded at start of session.
        if account.balance - amount < 0.00:
            self._print_message("Error: Insufficient funds.")
            return

        # --- Execution ---
        
        # Create transaction
        transaction = Withdrawal(holder_name, account_number, amount)
        self.transaction_list.append(transaction)
        
        # Update session totals (Standard only)
        if not self.session.is_admin():
            self.session.withdrawn_amount += amount
            
        self._print_message(f"Withdrawal of ${amount:.2f} successful.")

    def _handle_deposit(self) -> None:
        """
        Handles the 'deposit' transaction.
        
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
            self._print_message("Enter account holder name:")
            holder_name = self.read_line()
            
        # 2. Account Number
        self._print_message("Enter account number:")
        account_number = self.read_line()
        
        # 3. Amount
        self._print_message("Enter amount to deposit:")
        try:
            amount_str = self.read_line()
            amount = float(amount_str)
        except ValueError:
            self._print_message("Error: Invalid amount format.")
            return

        # --- Validation ---
        
        account = self.account_repository.find_account(account_number)
        if account is None:
            self._print_message("Error: Account not found.")
            return
            
        if account.holder_name != holder_name:
            self._print_message(f"Error: Account holder name '{holder_name}' does not match '{account.holder_name}'.")
            return

        # --- Execution ---
        
        transaction = Deposit(holder_name, account_number, amount)
        self.transaction_list.append(transaction)
        self._print_message(f"Deposit of ${amount:.2f} successful.")

    def _handle_paybill(self) -> None:
        """
        Handles the 'paybill' transaction.
        
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
            self._print_message("Enter account holder name:")
            holder_name = self.read_line()
            
        # 2. Account Number
        self._print_message("Enter account number:")
        account_number = self.read_line()
        
        # 3. Company
        self._print_message("Enter company name (EC, CQ, FI):")
        company = self.read_line()
        
        # 4. Amount
        self._print_message("Enter amount to pay:")
        try:
            amount_str = self.read_line()
            amount = float(amount_str)
        except ValueError:
            self._print_message("Error: Invalid amount format.")
            return

        # --- Validation ---
        
        account = self.account_repository.find_account(account_number)
        if account is None:
            self._print_message("Error: Account not found.")
            return
            
        if account.holder_name != holder_name:
            self._print_message("Error: Account holder name does not match.")
            return
            
        if company not in Paybill.COMPANIES:
             self._print_message("Error: Invalid company.")
             return

        # Check session limit (Standard only)
        if not self.session.is_admin():
            if self.session.paybill_amount + amount > 2000.00:
                self._print_message("Error: Session paybill limit ($2000) exceeded.")
                return
                
        # Check balance
        if account.balance - amount < 0.00:
            self._print_message("Error: Insufficient funds.")
            return

        # --- Execution ---
        
        transaction = Paybill(holder_name, account_number, company, amount)
        self.transaction_list.append(transaction)
        
        if not self.session.is_admin():
            self.session.paybill_amount += amount
            
        self._print_message(f"Paybill of ${amount:.2f} to {company} successful.")
            
    def _print_message(self, message):
        """
        Helper method to print a message to the console
        """
        print(message)

def main():
    """
    Entry point for the Banking System Front End.
    """
    app = ATMFrontEnd()
    app.start()

if __name__ == "__main__":
    main()
