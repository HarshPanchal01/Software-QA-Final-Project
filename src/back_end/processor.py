"""
Core processing logic for the Back End.
Parses the transaction file and applies transactions to the master accounts.
"""
from src.shared.directories import MASTER_BANK_ACCOUNTS_FILE
from src.shared.directories import CURRENT_BANK_ACCOUNTS_FILE
from src.shared.directories import MERGED_BANK_ACCOUNT_TRANSACTIONS_FILE
from typing import List, Dict
from src.back_end.read_write_bank_accounts import write_master_bank_accounts_file, write_current_bank_accounts_file, read_master_bank_accounts_file
from src.back_end.merged_transactions import merge_transactions, read_merged_transactions
from src.back_end.print_error import log_constraint_error
from src.shared.transactions import Transaction
from src.shared.bank_accounts import BankAccount

class BackendProcessor:

    def __init__(self):
        self.master_accounts: {} # empty dictionary

    def run(self):
        """Main execution flow for the backend."""
        # 1. Load current bank accounts from current master bank accounts file
        self.master_accounts = read_master_bank_accounts_file(MASTER_BANK_ACCOUNTS_FILE)

        # 2a. Create merged transactions file
        merge_transactions(MERGED_BANK_ACCOUNT_TRANSACTIONS_FILE)

        # 2b. Retreive all transactions as Transaction objects (ordered)
        transactions = read_merged_transactions(MERGED_BANK_ACCOUNT_TRANSACTIONS_FILE)

        # 3. Apply transactions (ordered)
        for tx in transactions:
            self.apply_transaction(tx)

        # 4. Write new master bank accounts file (accounts file used by backend)
        write_master_bank_accounts_file(self.master_accounts, MASTER_BANK_ACCOUNTS_FILE)
        # 5. Write current bank accounts after all transactions (accounts file used by frontend ATM)
        write_current_bank_accounts_file(self.master_accounts, CURRENT_BANK_ACCOUNTS_FILE)

    def apply_transaction(self, tx: Transaction) -> None:
        """Applies a single transaction to the corresponding account."""
        # tx.apply(self.master_accounts)