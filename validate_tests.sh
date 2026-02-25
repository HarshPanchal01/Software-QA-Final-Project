#!/bin/bash

# validate_tests.sh - Script to validate the output of qabank against expected outputs
# Requirements: Phase 3 (6) - Validate by comparing actual output transaction and terminal files to expected

EXPECTED_DIR="tests/expected_outputs"
ACTUAL_DIR="tests/actual_outputs"

echo "Validating test outputs..."

# Iterate through all generated .out terminal outputs
find "$ACTUAL_DIR" -type f -name "*.out" | sort | while read -r actual_out; do
    # Calculate relative paths to find expected counterparts
    rel_path="${actual_out#$ACTUAL_DIR/}"
    base_name=$(basename "$rel_path" .out)
    dir_name=$(dirname "$rel_path")
    
    expected_out="$EXPECTED_DIR/$dir_name/$base_name.out"
    actual_atf="$ACTUAL_DIR/$dir_name/$base_name.atf"
    expected_etf="$EXPECTED_DIR/$dir_name/$base_name.etf"
    
    echo "======================================================================"
    echo "Checking Test: $rel_path"
    
    # Check terminal output
    if [ ! -f "$expected_out" ]; then
        echo "  [SKIP] Terminal Log: No expected terminal output found."
    else
        diff_out=$(diff -u "$expected_out" "$actual_out")
        if [ $? -eq 0 ]; then
            echo "  [PASS] Terminal Log matches expected output."
        else
            echo "  [FAIL] Terminal Log mismatch!"
            echo "----------------------------------------"
            echo "$diff_out"
            echo "----------------------------------------"
        fi
    fi
    
    # Check transaction output
    if [ ! -f "$expected_etf" ]; then
        echo "  [SKIP] Transaction Log: No expected transaction output found."
    else
        diff_atf=$(diff -u "$expected_etf" "$actual_atf")
        if [ $? -eq 0 ]; then
            echo "  [PASS] Transaction Log matches expected output."
        else
            echo "  [FAIL] Transaction Log mismatch!"
            echo "----------------------------------------"
            echo "$diff_atf"
            echo "----------------------------------------"
        fi
    fi
    
done

echo "======================================================================"
echo "Validation completed."