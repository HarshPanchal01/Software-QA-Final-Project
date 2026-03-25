from src.shared.bank_accounts import SessionType

class Session:
    """
    Manages the state of the current user session.
    
    Intention:
        Tracks whether a user is logged in, their privileges (Standard vs Admin),
        and the session-specific totals (withdrawals, transfers, bill payments)
        to enforce daily limits defined in the requirements.
    
    Attributes:
        logged_in (bool): True if a user is currently authenticated.
        session_type (SessionType): STANDARD or ADMIN.
        current_user (str): Name of the currently logged-in account holder.
        withdrawn_amount (float): Total amount withdrawn in this session (limit $500).
        transferred_amount (float): Total amount transferred in this session (limit $1000).
        paybill_amount (float): Total amount paid to bills in this session (limit $2000).
    """
    def __init__(self) -> None:
        self.logged_in = False
        self.session_type = None
        self.current_user = ""
        # Session totals for standard mode limits
        self.withdrawn_amount = 0.0
        self.transferred_amount = 0.0
        self.paybill_amount = 0.0
        
    def login(self, session_type, current_user="") -> None:
        """
        Logs a user into the system.
        
        Intention:
            Sets the session state to active, stores the user's role and name,
            and resets all transaction limit counters to zero.
            
        Args:
            session_type (SessionType): The role of the user (Standard/Admin).
            current_user (str): The name of the account holder (optional for Admin).
        """
        self.logged_in = True
        self.session_type = session_type
        self.current_user = current_user
        # Reset totals on new login
        self.withdrawn_amount = 0.0
        self.transferred_amount = 0.0
        self.paybill_amount = 0.0
        
    def logout(self) -> None:
        """
        Logs the current user out.
        
        Intention:
            Resets the session state to its initial inactive state, clearing
            the current user and all session limit counters.
        """
        self.logged_in = False
        self.session_type = None
        self.current_user = ""
        self.withdrawn_amount = 0.0
        self.transferred_amount = 0.0
        self.paybill_amount = 0.0
        
    def is_admin(self) -> bool:
        """
        Checks if the current session has Admin privileges.
        
        Returns:
            bool: True if logged in as Admin, False otherwise.
        """
        return self.session_type == SessionType.ADMIN
    
    def is_logged_in(self) -> bool:
        """
        Checks if a user is currently logged in.
        
        Returns:
            bool: True if a session is active, False otherwise.
        """
        return self.logged_in
