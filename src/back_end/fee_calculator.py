from src.shared.bank_accounts import AccountPlan

class FeeCalculator:
    """
    Calculates transaction fees based on the account's plan.
    Student plan (SP): $0.05
    Non-student plan (NP): $0.10
    """
    @staticmethod
    def calculate(plan: AccountPlan) -> float:
        if plan == AccountPlan.STUDENT:
            return 0.05
        elif plan == AccountPlan.NON_STUDENT:
            return 0.10
        return 0.0  # Unknown plan type or default
