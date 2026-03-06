import os
from src.shared.bank_accounts import BankAccount, AccountFormat

def read_master_bank_accounts_file(file_path):
    """
    Reads the master bank accounts file (format with plan and transactions type)
    Returns list of accounts and prints fatal errors for invalid format
    """
    accounts = []
    try:
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                clean_line = line.rstrip('\n')
                
                try:
                    # convert account as a string into a BankAccount object
                    account = BankAccount.from_record(clean_line)
                    # EOF break
                    if account.account_number == "00000":
                        break
                    # add BankAccount object to cumulative list of all bank accounts
                    accounts.append(account)

                except Exception as e:
                    print(f"ERROR: Fatal error - Line {line_num}: Unexpected error - {str(e)}")
                    continue
    except FileNotFoundError:
        print(f"Warning: Master bank accounts file not found at {file_path}. Starting with an empty accounts list.")
        
    return accounts

def write_master_bank_accounts_file(accounts, file_path):
    """
    Writes master bank accounts file in backend format (45 chars)
    format_type: Backend format (45 chars):  NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP MM TTTT
    where MM is account plan (SP or NP), and TTTT is number of transactions on the account
    """

    # 1. ensure directory for file_path exists, create if not
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # 2. write to file
    with open(file_path, 'w') as file:
        for acc in accounts:
            try:
                # convert bank account object to a record (string) and append new line in the file
                file.write(acc.to_record(AccountFormat.BACKEND) + '\n')
                
            except Exception as e:
                print(f"ERROR: Unexpected error - {str(e)}")
                continue
        
        # Add END_OF_FILE marker
        file.write("00000 END_OF_FILE          A 00000.00 00 0000\n")

def write_current_bank_accounts_file(accounts, file_path):
    """
    Writes current bank accounts file in frontend format (37 chars)
    format_type: Backend format (45 chars):  NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP
    """

    # 1. ensure directory for file_path exists, create if not
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # 2. write to file
    with open(file_path, 'w') as file:
        for acc in accounts:
            try:
                # convert bank account object to a record (string) and append new line in the file
                file.write(acc.to_record(AccountFormat.FRONTEND) + '\n')
                
            except Exception as e:
                print(f"ERROR: Unexpected error - {str(e)}")
                continue
        
        # Add END_OF_FILE marker
        file.write("00000 END_OF_FILE          A 00000.00\n")