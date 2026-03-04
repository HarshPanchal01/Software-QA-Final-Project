"""
Entry point for the Back End application.
"""
import sys
import argparse
from src.back_end.processor import BackEndProcessor

def main():
    """
    Main function to parse arguments and run the backend processor.
    Expected usage:
        python -m src.back_end.main <old_master_file> <merged_transaction_file>
    """
    parser = argparse.ArgumentParser(description="Banking System Back End Processor")
    parser.add_argument("old_master", help="Path to the Old Master Bank Accounts File")
    parser.add_argument("merged_transactions", help="Path to the Merged Transaction File")
    
    args = parser.parse_args()
    
    try:
        processor = BackEndProcessor(args.old_master, args.merged_transactions)
        processor.run()
        print("Back End processing completed successfully.")
    except Exception as e:
        print(f"Fatal Error during Back End processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
