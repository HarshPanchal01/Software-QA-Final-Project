import os
from .models import BankAccount, AccountStatus

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
                line = line.strip('\n')
                
                # ignores a line that doesn't abide by the 37 character length account requirement
                if len(line) < 37 or len(line) > 37:
                    continue
                
                # parse account fields
                # account format (37 chars): NNNNN_AAAAAAAAAAAAAAAAAAAA_S_PPPPPPPP
                account_number = line[0:5]
                holder_name = line[6:26].rstrip()
                status_char = line[27]
                balance_string = line[29:37]
                
                if holder_name == "END_OF_FILE":
                    break
                
                # convert parsed values to intended typed variables
                # account_number and holder_name are left as strings
                status = AccountStatus.ACTIVE if status_char == 'A' else AccountStatus.DISABLED
                try:
                    balance = float(balance_string)
                except ValueError:
                    balance = 0.0
                
                # create the new runtime account
                account = BankAccount(account_number, holder_name, status, balance)
                # add the new runtime account to the AccountRepository's accounts
                self.accounts[account_number] = account
    
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
