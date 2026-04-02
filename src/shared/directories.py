

import os
from dataclasses import dataclass

"""
directory_config class

Keeps track of all the directories and files in the program.
Used to seperate different environments like testing and production.

"""

@dataclass
class directory_config:
    base_dir: str = os.environ.get("QABANK_DATA_DIR", "src/program_data")

    # Transactions
    @property
    def TRANSACTIONS_DIR(self): return f"{self.base_dir}/transactions/"
    @property
    def NEW_TRANSACTIONS_DIR(self): return f"{self.TRANSACTIONS_DIR}new/"
    @property
    def OLD_TRANSACTIONS_DIR(self): return f"{self.TRANSACTIONS_DIR}old/"
    @property
    def MERGED_TRANSACTIONS_DIR(self): return f"{self.TRANSACTIONS_DIR}merged/"
    @property
    def MERGED_BANK_ACCOUNT_TRANSACTIONS_FILE(self): return f"{self.MERGED_TRANSACTIONS_DIR}merged_bank_account_transactions_file.txt"
    
    # Bank Accounts
    @property
    def BANK_ACCOUNTS_DIR(self): return f"{self.base_dir}/bank_accounts/"
    @property
    def MASTER_BANK_ACCOUNTS_DIR(self): return f"{self.BANK_ACCOUNTS_DIR}master/"
    @property
    def CURRENT_BANK_ACCOUNTS_DIR(self): return f"{self.BANK_ACCOUNTS_DIR}current/"
    @property
    def MASTER_BANK_ACCOUNTS_FILE(self): return f"{self.MASTER_BANK_ACCOUNTS_DIR}master_bank_accounts.txt"
    @property
    def CURRENT_BANK_ACCOUNTS_FILE(self): return f"{self.CURRENT_BANK_ACCOUNTS_DIR}current_bank_accounts.txt"

config = directory_config()