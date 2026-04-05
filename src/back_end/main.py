"""
Entry point for the Back End application.
"""
import sys
import argparse
from src.back_end.processor import BackendProcessor

def main():
    """
    Main function to parse arguments and run the backend processor.
    Expected usage:
        python -m src.back_end.main <old_master_file>
    """
    parser = argparse.ArgumentParser(description="Banking System Back End Processor")
    
    args = parser.parse_args()
    
    try:
        processor = BackendProcessor()
        processor.run()
        # print("Back End processing completed successfully.")
    except Exception as e:
        print(f"Fatal Error during Back End processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
