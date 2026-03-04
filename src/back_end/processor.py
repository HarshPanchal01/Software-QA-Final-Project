"""
Core processing logic for the Back End.
Parses the transaction file and applies transactions to the master accounts.
"""
from typing import List, Dict
from src.back_end.models import MasterBankAccount, Transaction
from src.back_end.read import read_old_bank_accounts
from src.back_end.write import write_new_current_accounts
from src.back_end.print_error import log_constraint_error

class TransactionFileReader:
    @staticmethod
    def read_merged_transactions(filepath: str) -> List[Transaction]:
        """Reads and parses the merged transaction file."""
        transactions = []
        # TODO: Implement transaction parsing logic
        return transactions

class BackEndProcessor:
    def __init__(self, old_master_file: str, merged_transaction_file: str):
        self.old_master_file = old_master_file
        self.merged_transaction_file = merged_transaction_file
        self.master_accounts: Dict[str, MasterBankAccount] = {}

    def run(self):
        """Main execution flow for the backend."""
        # 1. Load accounts from old master file
        raw_accounts = read_old_bank_accounts(self.old_master_file)
        self.master_accounts = {
            acc['account_number']: MasterBankAccount(**acc) for acc in raw_accounts
        }

        # 2. Read merged transactions
        transactions = TransactionFileReader.read_merged_transactions(self.merged_transaction_file)

        # 3. Apply transactions
        for tx in transactions:
            self.apply_transaction(tx)

        # 4. Write new files
        self.write_current_accounts_file("new_current_accounts.txt")
        self.write_master_file("new_master_accounts.txt")

    def apply_transaction(self, tx: Transaction) -> None:
        """Applies a single transaction to the corresponding account."""
        # TODO: Implement transaction application logic with error handling
        pass

    def write_current_accounts_file(self, filepath: str) -> None:
        """Outputs the new current accounts file using the provided writer."""
        accounts_list = [
            {
                'account_number': acc.account_number,
                'name': acc.name,
                'status': acc.status,
                'balance': acc.balance,
                'total_transactions': acc.total_transactions,
                'plan': acc.plan
            }
            for acc in self.master_accounts.values()
        ]
        write_new_current_accounts(accounts_list, filepath)

    def write_master_file(self, filepath: str) -> None:
        """Outputs the new master accounts file (Phase 4 requirement)."""
        # TODO: Implement master file writer logic
        pass
