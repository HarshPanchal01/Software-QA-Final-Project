import os
from src.shared.bank_accounts import BankAccount, AccountStatus

class AccountRepository:
    """
    Manages the loading and retrieval of bank accounts from the file system.
    
    Intention:
        Reads the 'bank_accounts.txt' file, parses the fixed-width records into
        BankAccount objects, and provides methods to look up accounts by number
        and validate ownership.
        
    Attributes:
        accounts (dict): A dictionary mapping account numbers (str) to BankAccount objects.
    """
    def __init__(self):
        self.accounts = {}
        
    def load_from_file(self, filename) -> None:
        """
        Loads all bank accounts from the specified file into memory.
        
        Intention:
            Iterates through the file line by line.
            Parses each 37-character line into account details.
            Stops reading upon encountering "END_OF_FILE".
            Populates the self.accounts dictionary.
            
        Args:
            filename (str): Path to the bank accounts file.
        """
        if not os.path.exists(filename):
            return
        
        with open(filename, 'r') as file:
            for line in file:
                account = BankAccount.from_record(line)
                if int(account.account_number) <= 0 or len(account.account_number) > 5:
                    break
                self.accounts[account.account_number] = account
    
    def find_account(self, account_number) -> BankAccount | None:
        """
        Retrieves a bank account by its number.
        
        Args:
            account_number (str): The 5-digit account number.
            
        Returns:
            BankAccount | None: The account object if found, else None.
        """
        return self.accounts.get(account_number)

    def is_valid_owner(self, account_number, name) -> bool:
        """
        Validates if the provided name matches the account holder.
        
        Args:
            account_number (str): The account number to check.
            name (str): The name to verify.
            
        Returns:
            bool: True if the account exists and name matches, False otherwise.
        """
        account = self.find_account(account_number)
        if account is None:
            return False
        return account.holder_name == name
    
    def account_number_exists(self, account_number) -> bool:
        """
        Checks if an account number exists in the repository.
        
        Args:
            account_number (str): The account number to check.
            
        Returns:
            bool: True if the account exists, False otherwise.
        """
        return account_number in self.accounts
        
    def delete(self, account_number: str) -> None:
        """
        Removes an account from the repository.
        """
        if account_number in self.accounts:
            del self.accounts[account_number]
