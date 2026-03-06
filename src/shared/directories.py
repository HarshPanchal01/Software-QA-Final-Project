"""
Transactions directories & files
"""
TRANSACTIONS_DIR = "src/program_data/transactions/"
NEW_TRANSACTIONS_DIR = TRANSACTIONS_DIR + "new/" # all unprocessed transaction files from sessions are put into the 'new' directory
OLD_TRANSACTIONS_DIR = TRANSACTIONS_DIR + "old/" # all processed transaction files are put here (currently unused, as its not required)
MERGED_TRANSACTIONS_DIR = TRANSACTIONS_DIR + "merged/" # the merge transactions file lives in this directory
MERGED_BANK_ACCOUNT_TRANSACTIONS_FILE = MERGED_TRANSACTIONS_DIR + "merged_bank_account_transactions_file.txt" # exact file path to the merged transactions file

"""
Bank Accounts directories & files
"""
BANK_ACCOUNTS_DIR = "src/program_data/bank_accounts/"
MASTER_BANK_ACCOUNTS_DIR = BANK_ACCOUNTS_DIR + "master/" # bank accounts file used by the backend. includes # of transactions and student plan
CURRENT_BANK_ACCOUNTS_DIR = BANK_ACCOUNTS_DIR + "current/" # bank accounts file used by the frontend ATM. doesn't include # of transactions or student plan
MASTER_BANK_ACCOUNTS_FILE = MASTER_BANK_ACCOUNTS_DIR + "master_bank_accounts.txt" # back end accounts file
CURRENT_BANK_ACCOUNTS_FILE = CURRENT_BANK_ACCOUNTS_DIR + "current_bank_accounts.txt" # front end accounts file