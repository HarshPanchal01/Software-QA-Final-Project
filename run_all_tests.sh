#!/bin/bash

# Script to recursively run all test inputs against the qabank CLI.
# Usage: ./run_all_tests.sh

# 1. Check if qabank is installed
if ! command -v qabank &> /dev/null; then
    echo "Error: 'qabank' command not found."
    echo "Please install the project first using:"
    echo "  pip install -e ."
    exit 1
fi

TEST_DIR="tests/test_inputs"

if [ ! -d "$TEST_DIR" ]; then
    echo "Error: Test directory '$TEST_DIR' not found."
    exit 1
fi

echo "Starting Test Run..."
echo "======================================================================"

# 2. Find and run tests
find "$TEST_DIR" -type f -name "*.in.txt" | sort | while read -r INPUT_FILE; do
    echo "Testing Input: $INPUT_FILE"
    echo "----------------------------------------"
    
    # Run qabank with the input file
    qabank < "$INPUT_FILE"
    
    echo ""
    echo "----------------------------------------"
done

echo "======================================================================"
echo "All tests executed."
echo "Note: This script only RUNS the tests. It does not verify the output."
echo "Use 'pytest' for automated verification."
