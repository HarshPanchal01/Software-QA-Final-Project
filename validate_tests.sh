#!/bin/bash

# validate_tests.sh - Script to validate the output of qabank against expected outputs
# Requirements: Phase 3 (6) - Validate by comparing actual output transaction and terminal files to expected

EXPECTED_DIR="tests/expected_outputs"
ACTUAL_DIR="tests/actual_outputs"

GREEN=$'\033[0;32m'
RED=$'\033[0;31m'
YELLOW=$'\033[1;33m'
CYAN=$'\033[0;36m'
GRAY=$'\033[1;30m'
DEFAULT=$'\033[0m'

# ensure required directories exist before test validation
if [ ! -d "$EXPECTED_DIR" ]; then
    echo -e "${RED}Error: Expected directory not found: $EXPECTED_DIR${DEFAULT}"
    exit 1
fi
if [ ! -d "$ACTUAL_DIR" ]; then
    echo -e "${RED}Error: Actual output directory not found: $ACTUAL_DIR${DEFAULT}"
    echo "${YELLOW}Run ${GRAY}./run_tests.sh${YELLOW} first.${DEFAULT}"
    exit 1
fi

rows=() # global table rows for printing table info

# global values for testing summary
total=0
pass=0
fail=0
skip=0

# prints summary table
print_table() {
    local table_file=".validation_table.tsv" # temporary table file

    printf "Test Case\tTerminal\tTransaction\tOverall\n" > "$table_file" # table column names

    # print each row of data
    for row in "${rows[@]}"; do
        IFS='|' read -r test_name terminal_status transaction_status overall_status <<< "$row"
        printf "%s\t%s\t%s\t%s\n" "$test_name" "$terminal_status" "$transaction_status" "$overall_status" >> "$table_file"
    done

    # display test case and results, considers os/ps type
    if command -v pwsh > /dev/null 2>&1; then
        # modern powershell
        pwsh -NoProfile -Command '$rows = Import-Csv -Path ".validation_table.tsv" -Delimiter ([char]9); $rows | Format-Table -AutoSize'
    elif command -v powershell.exe > /dev/null 2>&1; then
        # windows powershell
        powershell.exe -NoProfile -Command "\$rows = Import-Csv -Path '.validation_table.tsv' -Delimiter ([char]9); \$rows | Format-Table -AutoSize"
    else
        # macOS / Linux: use printf with fixed-width columns to avoid ANSI color alignment issues
        local max_len=9
        for row in "${rows[@]}"; do
            IFS='|' read -r name _ _ _ <<< "$row"
            [ ${#name} -gt $max_len ] && max_len=${#name}
        done

        # header + separator
        printf "%-${max_len}s  %-12s %-12s %s\n" "Test Case" "Terminal" "Transaction" "Overall"
        printf "%-${max_len}s  %-12s %-12s %s\n" "---------" "--------" "-----------" "-------"

        for row in "${rows[@]}"; do
            IFS='|' read -r name term trans over <<< "$row"
            local pad=$((max_len - ${#name}))
            printf "%s%*s  %-23s %-23s %s\n" "$name" "$pad" "" "$term" "$trans" "$over"
        done
    fi

    # remove temp file
    rm -f "$table_file"
}

# helper method to check if 2 files are the same
# NOTE: since there are 2 different types of line endings (CRLF and LF), we treat both
#   as equal for compatibility. If we don't its likely (expected output != actual output)
_files_match() {
    # accept 2 input files
    local expected_file="$1"
    local actual_file="$2"

    # return 1 (false) if either file doesnt exist
    if [ ! -f "$expected_file" ] || [ ! -f "$actual_file" ]; then
        return 1
    fi

    # return 0 (true) if the files match (considering CRLF and LF as equal line-endings by removing them)
    if cmp -s <(tr -d '\r' < "$expected_file") <(tr -d '\r' < "$actual_file"); then
        return 0
    fi

    return 1
}

# gather all test names using all files included in testing (.out, .atf, .etf)
TEST_CASES=()
while IFS= read -r line; do
    TEST_CASES+=("$line")
done < <(
    {
        find "$ACTUAL_DIR"   -type f \( -name "*.out" -o -name "*.atf" \) -print
        find "$EXPECTED_DIR" -type f \( -name "*.out" -o -name "*.etf" \) -print
    } \
    | sed -E "s|^$ACTUAL_DIR/||" \
    | sed -E "s|^$EXPECTED_DIR/||" \
    | sed -E 's/\.(out|atf|etf)$//' \
    | sort -u
)
TOTAL_TESTS=${#TEST_CASES[@]}

i=0
for test in "${TEST_CASES[@]}"; do
    i=$((i + 1))
    # progress indicator (\033[K clears the rest of the line)
    printf "\r${CYAN}Validating test $i/$TOTAL_TESTS: (${test})${DEFAULT}\033[K"

    # Calculate relative paths to find expected counterparts
    base_name=$(basename "$test")
    dir_name=$(dirname "$test")
    test_name="$dir_name/$base_name"

    # base output directories
    actual_out="$ACTUAL_DIR/$dir_name/$base_name.out"
    expected_out="$EXPECTED_DIR/$dir_name/$base_name.out"

    actual_atf="$ACTUAL_DIR/$dir_name/$base_name.atf"
    expected_etf="$EXPECTED_DIR/$dir_name/$base_name.etf"

    # initial: set all tests as not found (skip)
    terminal_status="SKIP"
    transaction_status="SKIP"

    # terminal output validation + test status counting
    if [ -f "$expected_out" ] || [ -f "$actual_out" ]; then
        if _files_match "$expected_out" "$actual_out"; then
            terminal_status="PASS"
        else
            terminal_status="FAIL"
        fi
    fi

    # transaction output validation + test status counting
    if [ -f "$expected_etf" ] || [ -f "$actual_atf" ]; then
        if _files_match "$expected_etf" "$actual_atf"; then
            transaction_status="PASS"
        else
            transaction_status="FAIL"
        fi
    fi

    # final validation + summary data
    overall_status="PASS"

    # test final result
    total=$((total + 1))
    if [ "$terminal_status" = "FAIL" ] || [ "$transaction_status" = "FAIL" ]; then
        overall_status="FAIL"
        fail=$((fail + 1))
    elif [ "$terminal_status" = "SKIP" ] || [ "$transaction_status" = "SKIP" ]; then
        overall_status="SKIP"
        skip=$((skip + 1))
    else
        pass=$((pass + 1))
    fi

    # helper method to add color to a status
    _color_status() {
        case $1 in
            "PASS") echo -e "${GREEN}PASS${DEFAULT}" ;;
            "FAIL") echo -e "${RED}FAIL${DEFAULT}" ;;
            "SKIP") echo -e "${YELLOW}SKIP${DEFAULT}" ;;
        esac
    }
    # assign colors to each status (after text comparisons)
    terminal_status=$(_color_status "$terminal_status")
    transaction_status=$(_color_status "$transaction_status")
    overall_status=$(_color_status "$overall_status")


    rows+=("$test_name|$terminal_status|$transaction_status|$overall_status")
done

echo ""
print_table
echo -e "${CYAN}Summary ($total total tests):${DEFAULT} ${GREEN}$pass passed${DEFAULT}, ${RED}$fail failed${DEFAULT}, ${YELLOW}$skip skipped${DEFAULT}"

if [ "$fail" -gt 0 ]; then
    exit 1
fi
exit 0
