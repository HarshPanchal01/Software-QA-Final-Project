from enum import Enum

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
    ACTIVE = 'active'
    DISABLED = 'disabled'
    
class AccountPlan(Enum):
    """
    Enumeration for Bank Account Fee Plans.
    
    Intention:
        Distinguishes between 'Student' and 'Non-Student' plans.
        Used by the Back End to calculate transaction fees ($0.05 for Student, $0.10 for Non-Student).
    """
    STUDENT = 'SP'
    NON_STUDENT = 'NP'
    
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
    def __init__(self, account_number, holder_name, status, balance, plan=AccountPlan.NON_STUDENT):
        """
        Initializes a new BankAccount instance.
        
        Args:
            account_number (str): 5-digit string.
            holder_name (str): Account holder name.
            status (AccountStatus): Active or Disabled.
            balance (float): Monetary balance.
            plan (AccountPlan): Fee plan (default: Non-Student).
        """
        self.account_number = account_number
        self.holder_name = holder_name
        self.status = status
        self.balance = balance
        self.plan = plan
        
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
