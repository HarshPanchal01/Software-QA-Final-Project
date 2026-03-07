"""
    src/shared/transactions.py

    Transaction definitions shared between frontend and backend.
    Each transaction has a static method is_valid() that validates the transaction.
        (currently unused as validation is done in the front end and the project document
        states that the backend can assume all inputted files are valid)

"""

from src.shared.bank_accounts import BankAccount, SessionType
from src.back_end.fee_calculator import FeeCalculator
from typing import Dict

class Transaction():
    """
    Abstract base class for all system transactions.
    
    Intention:
        Defines the common attributes and behavior shared by all transaction types,
        specifically the ability to format themselves into a line for the 
        daily transaction record.
    
    Attributes:
        transaction_code (str): 2-digit identifier (e.g., "01" for Withdrawal).
        account_holder (str): Name involved in the transaction.
        account_number (str): Account number involved in the transaction.
        amount (float): Monetary value associated with the transaction.
        misc (str): Miscellaneous information needed for specific transactions.
        session_type (SessionType): Session type of the transaction.
    """
    def __init__(self, transaction_code, account_holder, account_number, amount, misc="", session_type=SessionType.STANDARD):
        self.transaction_code = transaction_code
        self.account_holder = account_holder
        self.account_number = account_number
        self.amount = amount
        self.misc = misc
        self.session_type = session_type
    
    def to_record(self) -> str:
        """
        Converts the transaction object into a string for the transaction record.
        """
        return self._format_record()
    
    @staticmethod
    def from_record(record: str):
        """
        Converts a string into a transaction object.
        """
        record = record.ljust(41, ' ')
        
        code = record[0:2]
        name = record[3:23].strip()
        number = record[24:29]
        amount = float(record[30:38])
        misc = record[39:41].strip()
        
        if code == "01": return Withdrawal(name, number, amount, misc)
        elif code == "02": return Transfer(name, number, amount, misc)
        elif code == "03": return Paybill(name, number, amount, misc)
        elif code == "04": return Deposit(name, number, amount, misc)
        elif code == "05": return CreateAccount(name, number, amount, misc)
        elif code == "06": return DeleteAccount(name, number, amount, misc)
        elif code == "07": return DisableAccount(name, number, amount, misc)
        elif code == "08": return ChangePlan(name, number, amount, misc)
        elif code == "00": return EndOfSession(name, number, amount, misc)
        else:
            return Transaction(code, name, number, amount, misc)

    def _format_record(self):
        """
        Helper to format the transaction fields into the fixed-width format.
        """
        code = self.transaction_code.zfill(2)
        name = self.account_holder.ljust(20, ' ')[:20]
        number = self.account_number.zfill(5)
        
        amount = "00000000" if self.amount == 0.0 else f"{self.amount:08.2f}"
        
        misc = "  " if self.misc.strip() == "" else self.misc[:2].ljust(2, ' ')
        return f"{code} {name} {number} {amount} {misc}"

    def __str__(self):
        return str(self.transaction_code) + " " + str(self.account_holder) + " " + str(self.account_number) + " " + str(self.amount) + " " + str(self.misc)

    def apply(self, master_accounts: Dict[str, BankAccount]) -> None:
        """Applies the transaction to the master accounts dictionary. To be overridden."""
        pass


class Withdrawal(Transaction):
    def __init__(self, account_holder, account_number, amount, misc=""):
        super().__init__("01", account_holder, account_number, amount, misc)

    def apply(self, master_accounts: Dict[str, BankAccount]) -> None:
        if self.account_number in master_accounts:
            acc = master_accounts[self.account_number]
            if acc.is_active():
                acc.balance -= self.amount
                fee = FeeCalculator.calculate(acc.plan)
                acc.apply_fee(fee)
                acc.increment_transaction_count()

class Transfer(Transaction):
    def __init__(self, account_holder, account_number, amount, misc=""):
        # misc stores the to_account_number
        super().__init__("02", account_holder, account_number, amount, misc)
    
    def apply(self, master_accounts: Dict[str, BankAccount]) -> None:
        to_account_number = self.misc.strip()
        if self.account_number in master_accounts and to_account_number in master_accounts:
            from_acc = master_accounts[self.account_number]
            to_acc = master_accounts[to_account_number]
            if from_acc.is_active() and to_acc.is_active():
                from_acc.balance -= self.amount
                to_acc.balance += self.amount
                fee = FeeCalculator.calculate(from_acc.plan)
                from_acc.apply_fee(fee)
                from_acc.increment_transaction_count()
    
class Paybill(Transaction):
    def __init__(self, account_holder, account_number, amount, misc=""):
        # misc stores the company name
        super().__init__("03", account_holder, account_number, amount, misc)

    def apply(self, master_accounts: Dict[str, BankAccount]) -> None:
        if self.account_number in master_accounts:
            acc = master_accounts[self.account_number]
            if acc.is_active():
                acc.balance -= self.amount
                fee = FeeCalculator.calculate(acc.plan)
                acc.apply_fee(fee)
                acc.increment_transaction_count()

class Deposit(Transaction):
    def __init__(self, account_holder, account_number, amount, misc=""):
        super().__init__("04", account_holder, account_number, amount, misc)

    def apply(self, master_accounts: Dict[str, BankAccount]) -> None:
        if self.account_number in master_accounts:
            acc = master_accounts[self.account_number]
            if acc.is_active():
                acc.balance += self.amount
                fee = FeeCalculator.calculate(acc.plan)
                acc.apply_fee(fee)
                acc.increment_transaction_count()
    
class CreateAccount(Transaction):
    def __init__(self, account_holder, account_number, amount, misc=""):
        # account_number might be "00000" in transaction file for create
        super().__init__("05", account_holder, account_number, amount, misc)

    def apply(self, master_accounts: Dict[str, BankAccount]) -> None:
        # Front end sends "00000" for the account number in the record, but in a real backend we might assign one.
        if self.account_number == "00000" or self.account_number == "":
            max_num = max([int(num) for num in master_accounts.keys() if num.isdigit() and num != "00000"] + [0])
            new_acc_num = str(max_num + 1).zfill(5)
        else:
            new_acc_num = self.account_number.zfill(5)

        from src.shared.bank_accounts import AccountStatus, AccountPlan
        master_accounts[new_acc_num] = BankAccount(
            account_number=new_acc_num,
            holder_name=self.account_holder,
            status=AccountStatus.ACTIVE,
            balance=self.amount,
            plan=AccountPlan.NON_STUDENT,
            transactions=0
        )
    
class DeleteAccount(Transaction):
    def __init__(self, account_holder, account_number, amount, misc=""):
        super().__init__("06", account_holder, account_number, amount, misc)

    def apply(self, master_accounts: Dict[str, BankAccount]) -> None:
        if self.account_number in master_accounts:
            del master_accounts[self.account_number]
    
class DisableAccount(Transaction):
    def __init__(self, account_holder, account_number, amount, misc=""):
        super().__init__("07", account_holder, account_number, amount, misc)

    def apply(self, master_accounts: Dict[str, BankAccount]) -> None:
        if self.account_number in master_accounts:
            from src.shared.bank_accounts import AccountStatus
            master_accounts[self.account_number].status = AccountStatus.DISABLED
    
class ChangePlan(Transaction):
    def __init__(self, account_holder, account_number, amount, misc=""):
        super().__init__("08", account_holder, account_number, amount, misc)
    
    def apply(self, master_accounts: Dict[str, BankAccount]) -> None:
        if self.account_number in master_accounts:
            from src.shared.bank_accounts import AccountPlan
            acc = master_accounts[self.account_number]
            if acc.plan == AccountPlan.STUDENT:
                acc.plan = AccountPlan.NON_STUDENT
            else:
                acc.plan = AccountPlan.STUDENT

class EndOfSession(Transaction):
    def __init__(self, account_holder="", account_number="00000", amount=0.0, misc=""):
        super().__init__("00", account_holder, "00000", 0.0, misc)
    
    def apply(self, master_accounts: Dict[str, BankAccount]) -> None:
        pass