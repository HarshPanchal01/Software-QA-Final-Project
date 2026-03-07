import os
from src.shared.transactions import Transaction
from src.shared.directories import NEW_TRANSACTIONS_DIR

class MergedTransactions:
    @staticmethod
    def merge_transactions(file_path: str) -> None:
        """
        Reads transactions from all transaction files (in src/transactions/new) and merges
            them into a single file

        Args:
            file_path (str): Path to the merged transactions file

        Note: this method doesn't exclude transaction '00', since it is a simple
            merger of all transaction files. Use of the merged transactions file
            must account for this (e.g. by ignoring transaction '00').
        """
        # 1. ensure merge file directory exists, create it if not
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 2. read and merge transactions
        try:
            # 1. Gather all transaction files in src/transactions/new in order (ascending)
            os.makedirs(NEW_TRANSACTIONS_DIR, exist_ok=True)
            transaction_files = sorted([f for f in os.listdir(NEW_TRANSACTIONS_DIR) if f.endswith(".txt")])

            # 2. In order (ascending), read each file and write its lines into the merged file
            with open(file_path, "w") as merged_file:
                for file in transaction_files:
                    saw_EOF = False # marker to denote when we can delete the transaction file after reading
                    with open(f"{NEW_TRANSACTIONS_DIR}{file}", "r") as f:
                        for line in f:
                            transaction = Transaction.from_record(line)
                            # ignore EOF markers for each individual transaction file
                            if transaction.transaction_code == "00":
                                saw_EOF = True
                                break

                            merged_file.write(line)
                    # delete the file now that we have read it
                    if saw_EOF:
                        os.remove(f"{NEW_TRANSACTIONS_DIR}{file}")
                # write EOF marker at the end of the merged transactions file
                merged_file.writelines("00                      00000 00000000   \n")
        except Exception as e:
            print(f"ERROR: Unexpected error while merging transactions - {str(e)}")
            return
    
    @staticmethod
    def read_merged_transactions(file_path: str) -> list[Transaction]:
        """
        Reads transactions from the merged transactions file and returns a list of transaction objects
        """
        transactions = []

        try:
            # 1. Read: convert each line from each file into a transaction and add to ordererd list
            with open(file_path, "r") as merged_file:
                for line in merged_file:
                    # convert transaction string from file to a transaction object
                    transaction = Transaction.from_record(line)
                    # EOF break
                    if transaction.transaction_code == "00":
                        break
                    transactions.append(transaction)

        except Exception as e:
            print(f"ERROR: Unexpected error while reading merged transactions file - {str(e)}")
            return []

        return transactions