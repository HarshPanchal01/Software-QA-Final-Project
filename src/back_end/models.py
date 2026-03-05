"""
Data models for the Back End.
Includes representations of Bank Accounts and Transactions.
"""
from dataclasses import dataclass
from typing import Dict

@dataclass
class MasterBankAccount:
    account_number: str
    holder_name: str
    status: str
    balance: float
    plan: str
    transaction_count: int

    def is_active(self) -> bool:
        return self.status == 'A'

    def is_student_plan(self) -> bool:
        return self.plan == 'SP'

    def apply_fee(self) -> None:
        """Applies the transaction fee based on the account plan."""
        pass # To be implemented based on FeeCalculator

    def increment_transaction_count(self) -> None:
        """Increments the transaction count."""
        self.transaction_count += 1

class Transaction:
    """Base class for all transactions to be processed by the backend."""
    def __init__(self, transaction_code: str, account_holder_name: str, account_number: str, amount: float, session_type: str = "Standard", misc: str = ""):
        self.transaction_code = transaction_code
        self.account_holder_name = account_holder_name
        self.account_number = account_number
        self.amount = amount
        self.session_type = session_type
        self.misc = misc

    def apply(self, master_accounts: Dict[str, MasterBankAccount]) -> None:
        """Applies the transaction to the overall dictionary of master accounts. To be overridden."""
        pass
