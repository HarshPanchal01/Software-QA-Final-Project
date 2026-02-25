#!/bin/bash

# run_tests.sh - Script to automate testing of the qabank application
# Requirements: Phase 3 (5) - Run program on each input file, create corresponding output files (terminal and transaction)

# Ensure qabank is installed
if ! command -v qabank &> /dev/null; then
    echo "Error: 'qabank' command not found. Please run 'pip install -e .'"
    exit 1
fi

INPUT_DIR="tests/test_inputs"
OUTPUT_DIR="tests/actual_outputs"
ACCOUNTS_FILE="bank_accounts.txt"

echo "Starting automated tests..."

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
    
    echo "Running test: $rel_path"
    
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

echo "Automated testing completed. Outputs saved to $OUTPUT_DIR/"