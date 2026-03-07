from __future__ import annotations
from enum import Enum

"""
    src/shared/bank_accounts.py

    Bank account data classes shared between the frontend and backend.

    Data classes:
        - SessionType: indicates admin vs. standard user
        - AccountStatus: indicates whether an account is disabled or active
        - AccountPlan: indicates student plan vs. non-student plan
        - AccountFormat: indicates frontend vs backend fixed-width formats
        - BankAccount: snapshot data of a bank account
"""


class SessionType(Enum):
    """
    Enumeration for User Session Types.
    
    Intention:
        Distinguishes between 'Standard' (regular user) and 'Admin' (privileged user)
        sessions to control access to specific commands (e.g., create, delete).
    """
    STANDARD = 'standard'
    ADMIN = 'admin'

class AccountStatus(Enum):
    """
    Enumeration for Bank Account Status.
    
    Intention:
        Indicates whether a bank account is currently 'Active' (can perform transactions)
        or 'Disabled' (cannot perform transactions).
    """
    ACTIVE = 'A'
    DISABLED = 'D'
    UNKNOWN = '0' # used for EOF marker and to indicate unknown status
    
class AccountPlan(Enum):
    """
    Enumeration for Bank Account Fee Plans.
    
    Intention:
        Distinguishes between 'Student' and 'Non-Student' plans.
        Used by the Back End to calculate transaction fees ($0.05 for Student, $0.10 for Non-Student).
    """
    STUDENT = 'SP'
    NON_STUDENT = 'NP'
    UNKNOWN = '00' # used for EOF marker and to indicate unknown plan

class AccountFormat(Enum):
    BACKEND = 'backend'
    FRONTEND = 'frontend'
    
class BankAccount:
    """
    Represents a snapshot of a Bank Account loaded from the accounts file.
    
    Intention:
        Stores the state of a single bank account (number, holder, balance, status)
        in memory to validate transactions (e.g., checking for sufficient funds,
        verifying ownership) during the Front End session.
    
    Attributes:
        account_number (str): The unique 5-digit account number.
        holder_name (str): The name of the account holder (max 20 chars).
        status (AccountStatus): The current status (Active/Disabled).
        balance (float): The current balance in the account.
        plan (AccountPlan): The fee plan associated with the account.
    """
    def __init__(self, account_number, holder_name, status, balance, plan=None, transactions=None):
        """
        Initializes a new BankAccount instance.
        
        Args:
            account_number (str): 5-digit string.
            holder_name (str): Account holder name.
            status (AccountStatus): Active or Disabled.
            balance (float): Monetary balance.
            plan (AccountPlan): Fee plan (default: Non-Student).
            transactions(): number of transactions recorded on the account
        """
        self.account_number = account_number
        self.holder_name = holder_name
        self.status = status
        self.balance = balance
        self.plan = plan
        self.transactions = transactions
        
    def is_active(self) -> bool:
        """
        Checks if the account is active.
        
        Returns:
            bool: True if status is ACTIVE, False otherwise.
        """
        return self.status == AccountStatus.ACTIVE
    
    def is_student_plan(self) -> bool:
        """
        Checks if the account is on the student plan.
        
        Returns:
            bool: True if plan is STUDENT, False otherwise.
        """
        return self.plan == AccountPlan.STUDENT

    def increment_transaction_count(self) -> None:
        """Increments the transaction count for this account."""
        if self.transactions is not None:
            self.transactions += 1

    def apply_fee(self, fee_amount: float) -> None:
        """Applies a fee to the account balance."""
        self.balance -= fee_amount
    
    def to_record(self, format_type: AccountFormat) -> str | None:
        """
        Converts the bank account object into a string for the bank account record.
        
        Args:
            format_type (str): "frontend" (current) or "backend" (master).
                Frontend format (37 chars): NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP
                Backend format (45 chars):  NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP MM TTTT

        Returns:
            str: The formatted string record.
        """
        try:
            account_number = self.account_number.zfill(5)
            holder_name = self.holder_name.ljust(20, ' ')[:20]
            status = self.status.value
            balance = f"{self.balance:08.2f}"
            
            if format_type == AccountFormat.BACKEND:
                plan = self.plan.value
                transactions = str(self.transactions).zfill(4)
                # return backend (master) format
                return f"{account_number} {holder_name} {status} {balance} {plan} {transactions}"
            # return frontent (current) format
            return f"{account_number} {holder_name} {status} {balance}"
        except Exception as e:
            print(f"ERROR - formatting bank account object to string: {str(e)}")
            return None
    
    @classmethod
    def from_record(cls, record: str) -> BankAccount | None:
        """
        Converts a string into a bank account object.
        Detects account format based on length:
            format_type:
                Frontend format (37 chars): NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP
                Backend format (45 chars):  NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP MM TTTT
        by inspecting the length of the record provided!
        
        Args:
            record (str): The string record from a file.
        """
        clean_record = record.rstrip('\n')
        try:
            account_number = clean_record[0:5].strip()
            holder_name = clean_record[6:26].strip()
            status_char = clean_record[27]
            status = AccountStatus(status_char) if status_char.strip() else AccountStatus.UNKNOWN
            balance = float(clean_record[29:37])
        
            # Backend format: special extractions
            if len(clean_record) >= 45:
                plan_str = clean_record[38:40].strip()
                plan = AccountPlan(plan_str) if plan_str else AccountPlan.UNKNOWN
                transactions_str = clean_record[41:45].strip()
                transactions = int(transactions_str) if transactions_str.isdigit() else 0
            # Frontend format: leave as None, they should never be accessed anyway
            else:
                plan = AccountPlan.UNKNOWN
                transactions = 0
            
        except Exception as e:
            print(f"ERROR - formatting string to bank account object: {str(e)}")
            return None
            
        return cls(account_number, holder_name, status, balance, plan, transactions)