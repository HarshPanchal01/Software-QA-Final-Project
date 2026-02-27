#!/bin/bash

# run_tests.sh - Script to automate testing of the qabank application
# Requirements: Phase 3 (5) - Run program on each input file, create corresponding output files (terminal and transaction)

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

INPUT_DIR="tests/test_inputs"
OUTPUT_DIR="tests/actual_outputs"
ACCOUNTS_FILE="bank_accounts.txt"

echo "${CYAN}Starting automated tests...${DEFAULT}"

# Clean or create output directory
if [ -d "$OUTPUT_DIR" ]; then
    rm -rf "$OUTPUT_DIR"
fi
mkdir -p "$OUTPUT_DIR"

# Find all test inputs and run the program
find "$INPUT_DIR" -type f -name "*.in.txt" | sort | while read -r input_file; do
    # Calculate relative paths to maintain directory structure
    rel_path="${input_file#$INPUT_DIR/}"
    dir_name=$(dirname "$rel_path")
    base_name=$(basename "$rel_path" .in.txt)
    
    # Create matching output subdirectories
    mkdir -p "$OUTPUT_DIR/$dir_name"
    
    # Define actual output files
    actual_out="$OUTPUT_DIR/$dir_name/$base_name.out"
    actual_atf="$OUTPUT_DIR/$dir_name/$base_name.atf"
    
    echo "${CYAN}Running test: ${GRAY}$rel_path${DEFAULT}"
    
    # Remove old transaction file if exists locally just in case
    rm -f "$actual_atf"
    
    # Run qabank with command line arguments (accounts file, output transaction file)
    # Redirect standard input to input file, and standard output to output file
    qabank "$ACCOUNTS_FILE" "$actual_atf" < "$input_file" > "$actual_out"
    
    # Strip terminal colors from output using sed for comparison later
    sed -i -e 's/\x1b\[[0-9;]*m//g' "$actual_out"
    
    # If the transaction file was not created, create an empty one for uniform comparison
    if [ ! -f "$actual_atf" ]; then
        touch "$actual_atf"
    fi
done

echo "${CYAN}Automated testing completed. Outputs saved to ${GRAY}$OUTPUT_DIR/${DEFAULT}"