#!/bin/bash

# weekly.sh - Script to automate weekly operations of the qabank application
# Requirements: Phase 6 (2) - Runs daily.sh script for 7 days. This simulates 
#               the bank running daily operations each day for a week.

GREEN=$'\033[0;32m'
RED=$'\033[0;31m'
YELLOW=$'\033[1;33m'
CYAN=$'\033[0;36m'
GRAY=$'\033[1;30m'
DEFAULT=$'\033[0m'

# Ensure qabank is installed
if ! command -v qabank &> /dev/null; then
    echo -e "${RED}Error: 'qabank' command not found. Please run ${GRAY}pip install -e .${DEFAULT}"
    exit 1
fi

# path to canonical bank accounts files
CURRENT_ACCOUNTS="src/program_data/bank_accounts/current/current_bank_accounts.txt"
MASTER_ACCOUNTS="src/program_data/bank_accounts/master/master_bank_accounts.txt"

echo -e "${CYAN}Starting Weekly Operations (7 Days)${DEFAULT}"

# Setup Day 0 accounts
echo -e "${GRAY}Initializing Day 0 accounts...${DEFAULT}"
cp "tests/test_data/bank_accounts/current/current_bank_accounts.txt" "$CURRENT_ACCOUNTS"
cp "tests/test_data/bank_accounts/master/master_bank_accounts.txt" "$MASTER_ACCOUNTS"

# loop run daily.sh script for 7 days
for day in {1..7}; do
    DAY_DIR="sessions/day${day}"
    
    # early out if the sessions directory doesnt exist
    if [ ! -d "$DAY_DIR" ]; then
        echo -e "${RED}Error: Directory '$DAY_DIR' not found. Cannot proceed with weekly run.${DEFAULT}"
        break
    fi

    # progress indicator
    i=$((i + 1)) 
    printf "\r${CYAN}Running day $i/7: (${DAY_DIR})${DEFAULT}\033[K"
    
    # run the daily script for the current day
    # ('true' = silent mode, no output from ./daily.sh except for errors)
    bash daily.sh "$DAY_DIR" true
done

echo ""
echo -e "${GREEN}Weekly Operations Completed Successfully. Check ${GRAY}${CURRENT_ACCOUNTS}${GREEN} and ${GRAY}${MASTER_ACCOUNTS}${GREEN} for the updated account information.${DEFAULT}"
