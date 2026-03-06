"""
    src/shared/transactions.py

    Transaction definitions shared between frontend and backend.
    Each transaction has a static method is_valid() that validates the transaction.
        (currently unused as validation is done in the front end and the project document
        states that the backend can assume all inputted files are valid)

"""

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
    """
    def __init__(self, transaction_code, account_holder, account_number, amount, misc=""):
        self.transaction_code = transaction_code
        self.account_holder = account_holder
        self.account_number = account_number
        self.amount = amount
        self.misc = misc
    
    def to_record(self) -> str:
        """
        Converts the transaction object into a string for the transaction record.
        
        Args:
            miscellaneous (str): Extra info needed for specific transactions.

        Returns:
            str: The formatted 40-character (plus newline) string record.
        """
        return self._format_record()
    
    @classmethod
    def from_record(cls, record: str):
        """
        Converts a string into a transaction object.
        
        Args:
            record (str): The 41 character (plus newline) string record.
        """
        return cls._unformat_record(record)
    
    @classmethod
    def _unformat_record(cls, record: str):
        """
        Converts a string into a transaction object.
        
        Args:
            record (str): The 41 character (plus newline) string record.
        
        Warning:
            Will unformat end of file marker as a transaction.
            Be sure to handle this (easiest: if code == "00", break)
        """
        # ensure record is long enough to prevent index errors
        record = record.ljust(41, ' ')
        
        code = record[0:2]
        name = record[3:23].strip()
        number = record[24:29]
        amount = float(record[30:38])
        misc = record[39:41].strip()
        
        return cls(code, name, number, amount, misc)

    def _format_record(self):
        """
        Helper to format the transaction fields into the fixed-width format.
        
        Format: CC_AAAAAAAAAAAAAAAAAAAA_NNNNN_PPPPPPPP_MM
        
        Args:
            miscellaneous (str): Extra info needed for specific transactions (e.g., company code).
            
        Returns:
            str: The fully formatted line.
        """
        code = self.transaction_code.zfill(2)
        name = self.account_holder.ljust(20, ' ')[:20]
        number = self.account_number.zfill(5)
        
        amount = "00000000" if self.amount == 0.0 else f"{self.amount:08.2f}"
        
        misc = "  " if self.misc.strip() == "" else self.misc[:2].ljust(2, ' ')
        return f"{code} {name} {number} {amount} {misc}"

    def __str__(self):
        """
        Standard string representation of the transaction object
        """
        return str(self.transaction_code) + " " + str(self.account_holder) + " " + str(self.account_number) + " " + str(self.amount) + " " + str(self.misc)


class Withdrawal(Transaction):
    """
    Represents a withdrawal transaction (Code 01).
    Intention: Deducts funds from an account.
    """
    def __init__(self, account_holder, account_number, amount):
        super().__init__("01", account_holder, account_number, amount)

    def to_file_record(self) -> str: return self._format_record()

class Transfer(Transaction):
    """
    Represents a transfer transaction (Code 02).
    Intention: Moves funds from one account to another.
    """
    def __init__(self, account_holder, account_number, to_account_number, amount):
        super().__init__("02", account_holder, account_number, amount, to_account_number)
    
    def to_file_record(self) -> str: return self._format_record()
    
class Paybill(Transaction):
    """
    Represents a paybill transaction (Code 03).
    Intention: Pays a bill to a specific company (EC, CQ, FI).
    """
    COMPANIES = {
        "EC": "The Bright Light Electric Company",
        "CQ": "Credit Card Company",
        "FI": "Fast Internet, Inc."
    }
    
    def __init__(self, account_holder, account_number, company_name, amount):
        super().__init__("03", account_holder, account_number, amount, company_name)

    def to_file_record(self) -> str: return self._format_record()

class Deposit(Transaction):
    """
    Represents a deposit transaction (Code 04).
    Intention: Adds funds to an account.
    """
    def __init__(self, account_holder, account_number, amount):
        super().__init__("04", account_holder, account_number, amount)

    def to_file_record(self) -> str: return self._format_record()
    
class Create(Transaction):
    """
    Represents a create transaction (Code 05).
    Intention: Creates a new bank account with an initial balance.
    """
    def __init__(self, account_holder, initial_balance):
        super().__init__("05", account_holder, "00000", initial_balance)
        self.initial_balance = initial_balance

    def to_file_record(self) -> str: return self._format_record()
    
class Delete(Transaction):
    """
    Represents a delete transaction (Code 06).
    Intention: Deletes an existing bank account.
    """
    def __init__(self, account_holder, account_number):
        super().__init__("06", account_holder, account_number, 0.0)

    def to_file_record(self) -> str: return self._format_record()
    
class Disable(Transaction):
    """
    Represents a disable transaction (Code 07).
    Intention: Disables an account, preventing further transactions.
    """
    def __init__(self, account_holder, account_number):
        super().__init__("07", account_holder, account_number, 0.0)

    def to_file_record(self) -> str: return self._format_record()
    
class ChangePlan(Transaction):
    """
    Represents a changeplan transaction (Code 08).
    Intention: Toggles the fee plan (Student <-> Non-Student).
    """
    def __init__(self, account_holder, account_number):
        super().__init__("08", account_holder, account_number, 0.0)
    
    def to_file_record(self) -> str: return self._format_record()

class EndOfSession(Transaction):
    """
    Represents the End of Session marker (Code 00).
    Intention: Marks the end of the transaction file.
    """
    def __init__(self, account_holder=""):
        super().__init__("00", account_holder, "00000", 0.0)
    
    def to_file_record(self) -> str: return self._format_record()