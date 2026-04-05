#!/bin/bash

# daily.sh - Script to automate daily operations of the qabank application
# Requirements: Phase 6 (1) - Runs the front end for each session file in a defined
#       folder, then runs the back end to merge and process the transactions.

GREEN=$'\033[0;32m'
RED=$'\033[0;31m'
YELLOW=$'\033[1;33m'
CYAN=$'\033[0;36m'
GRAY=$'\033[1;30m'
DEFAULT=$'\033[0m'

SESSIONS_DIR=$1
SILENT_MODE=$2

# helper for logging non-error messages
print_message() {
    if [ "$SILENT_MODE" != "true" ]; then
        echo -e "$@"
    fi
}

# early out if the sessions directory doesnt exist
if [ ! -d "$SESSIONS_DIR" ]; then
    echo -e "${RED}Error: Directory '$SESSIONS_DIR' was not found.${DEFAULT}"
    exit 1
fi

# define file paths (canonical paths, not testing paths)
CURRENT_ACCOUNTS="src/program_data/bank_accounts/current/current_bank_accounts.txt"
MASTER_ACCOUNTS="src/program_data/bank_accounts/master/master_bank_accounts.txt"
TRANSACTIONS_DIR="src/program_data/transactions/new"

# create the transactions directory if it doesnt exist
mkdir -p "$TRANSACTIONS_DIR"

print_message "${CYAN}Starting daily run... ${GRAY}$SESSIONS_DIR${DEFAULT}"

# ensure *.in.txt isn't taken literally if no files exist
shopt -s nullglob
session_files=("$SESSIONS_DIR"/*.in.txt)
shopt -u nullglob

# early out if the sessions directory doesnt contain any session files
if [ ${#session_files[@]} -eq 0 ]; then
    echo -e "${RED}No session files (*.in.txt) found in $SESSIONS_DIR.${DEFAULT}"
    exit 1
fi

for session_file in "${session_files[@]}"; do
    base_name=$(basename "$session_file" .in.txt)
    output_tx_file="$TRANSACTIONS_DIR/${base_name}_txn.txt"
    
    # run the front end
    print_message "${CYAN}Running front end for session: ${GRAY}$session_file${DEFAULT}"
    qabank "$CURRENT_ACCOUNTS" "$output_tx_file" < "$session_file" > /dev/null
    
    # ensure transaction file was created
    if [ ! -f "$output_tx_file" ]; then
        echo -e "${YELLOW}Warning: No transaction file generated for $session_file${DEFAULT}"
    fi
done

# run the backend
print_message "${CYAN}Running backend...${DEFAULT}"
python -m src.back_end.main

if [ $? -eq 0 ]; then
    print_message "${GREEN}Daily run completed successfully.${DEFAULT}"
else
    echo -e "${RED}Error: Backend failed${DEFAULT}"
    exit 1
fi

