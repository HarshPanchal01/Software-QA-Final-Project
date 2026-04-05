"""
Core processing logic for the Back End.
Parses the transaction file and applies transactions to the master accounts.
"""
from src.shared.directories import config
from typing import List, Dict
from src.back_end.read_write_bank_accounts import BankAccountFileIO
from src.back_end.merged_transactions import MergedTransactions
from src.back_end.print_error import log_constraint_error
from src.shared.transactions import Transaction
from src.shared.bank_accounts import BankAccount

class BackendProcessor:

    def __init__(self) -> None:
        self.master_accounts: Dict[str, BankAccount] = {}

    def run(self) -> None:
        """Main execution flow for the backend."""
        # 1. Load current bank accounts from current master bank accounts file
        self.master_accounts = BankAccountFileIO.read_master_accounts(config.MASTER_BANK_ACCOUNTS_FILE)

        # 2a. Create merged transactions file
        MergedTransactions.merge_transactions(config.MERGED_BANK_ACCOUNT_TRANSACTIONS_FILE)

        # 2b. Retreive all transactions as Transaction objects (ordered)
        transactions = MergedTransactions.read_merged_transactions(config.MERGED_BANK_ACCOUNT_TRANSACTIONS_FILE)

        # 3. Apply transactions (ordered)
        for tx in transactions:
            self.apply_transaction(tx)

        # 4. Write new master bank accounts file (accounts file used by backend)
        BankAccountFileIO.write_master_accounts(self.master_accounts, config.MASTER_BANK_ACCOUNTS_FILE)
        # 5. Write current bank accounts after all transactions (accounts file used by frontend ATM)
        BankAccountFileIO.write_current_accounts(self.master_accounts, config.CURRENT_BANK_ACCOUNTS_FILE)

    def apply_transaction(self, tx: Transaction) -> None:
        """Applies a single transaction to the corresponding account."""
        tx.apply(self.master_accounts)