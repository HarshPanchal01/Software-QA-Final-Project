#!/bin/bash

# daily.sh
# Orchestrates a single day of banking operations.
# Usage: ./daily.sh <input_sessions_directory>

GREEN=$'\033[0;32m'
CYAN=$'\033[0;36m'
DEFAULT=$'\033[0m'

INPUT_DIR=$1
TRANSACTIONS_DIR="src/program_data/transactions/new"
CURRENT_ACCOUNTS="src/program_data/bank_accounts/current/current_bank_accounts.txt"

# 1. Validate Input
if [ -z "$INPUT_DIR" ]; then
    echo "Usage: ./daily.sh <input_sessions_directory>"
    exit 1
fi

if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Directory $INPUT_DIR not found."
    exit 1
fi

echo "${CYAN}=== Starting Daily Banking Operations ===${DEFAULT}"

# 2. Ensure transactions output directory exists and is empty from previous day
mkdir -p "$TRANSACTIONS_DIR"
rm -f "$TRANSACTIONS_DIR"/*.txt

# 3. Run Front End for each session file in the directory
counter=1
for session_file in "$INPUT_DIR"/*.txt; do
    if [ -f "$session_file" ]; then
        echo "Running ATM Session $counter: $(basename "$session_file")"
        
        output_transaction_file="$TRANSACTIONS_DIR/$counter.txt"
        
        # Run qabank (Front End) mapping stdin to the session file and output to the new transactions folder
        # We redirect stdout to /dev/null so the terminal doesn't get flooded with ATM prompts
        ./sqa_final_project_venv/bin/qabank "$CURRENT_ACCOUNTS" "$output_transaction_file" < "$session_file" > /dev/null
        
        counter=$((counter + 1))
    fi
done

# 4. Run Back End Processor
echo "${CYAN}--- All ATM sessions complete. Running Daily Batch Processor ---${DEFAULT}"
# The python script automatically merges the files in $TRANSACTIONS_DIR and updates the master accounts
python3 -m src.back_end.main

echo "${GREEN}=== Daily Operations Complete! ===${DEFAULT}"
