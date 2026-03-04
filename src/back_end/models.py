"""
Data models for the Back End.
Includes representations of Bank Accounts and Transactions.
"""
from dataclasses import dataclass

@dataclass
class MasterBankAccount:
    account_number: str
    name: str
    status: str
    balance: float
    total_transactions: int
    plan: str

    def is_active(self) -> bool:
        return self.status == 'A'

    def is_student_plan(self) -> bool:
        return self.plan == 'SP'

class Transaction:
    """Base class for all transactions to be processed by the backend."""
    def __init__(self, transaction_code: str, account_holder_name: str, account_number: str, amount: float, misc: str = ""):
        self.transaction_code = transaction_code
        self.account_holder_name = account_holder_name
        self.account_number = account_number
        self.amount = amount
        self.misc = misc

    def apply(self, account: MasterBankAccount) -> None:
        """Applies the transaction to the given MasterBankAccount. To be overridden by subclasses."""
        pass
