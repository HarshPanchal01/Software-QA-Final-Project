# Software QA Final Project - Banking System

This project is a CLI-based Banking System developed for CSCI 3060U. It consists of a Front End (ATM) and Back End (Batch Processor), adhering to strict input/output constraints.

## Table of Contents
- [Developer Setup](#developer-setup)
- [Usage (Phase 2 - Front End)](#3-usage-phase-2---front-end)
- [Input/Output (Phase 2)](#inputoutput-phase-2)
- [Commiting to GitHub repo](#4-commiting-to-github-repo)

## Developer Setup

To ensure all developers are using the same environment, please follow these steps:

### 1. Prerequisites
- Python 3.12+ installed

### 2. Environment Setup

**Linux / Mac:**
```bash
# Create the virtual environment (one time only)
python3 -m venv sqa_final_project_venv

# Activate the virtual environment
source sqa_final_project_venv/bin/activate

# Install dependencies & Install CLI tool in editable mode
pip3 install -r requirements.txt
pip3 install -e .
```

**Windows:**
```cmd
:: Create the virtual environment (one time only)
python -m venv sqa_final_project_venv

:: Activate the virtual environment
sqa_final_project_venv\Scripts\activate

:: Install dependencies & Install CLI tool in editable mode
pip install -r requirements.txt
pip install -e .
```

### 3. Usage (Phase 2 & 3 - Front End)

Once installed (via `pip install -e .`), you can run the application directly from your terminal:

```bash
# Basic usage (defaults to bank_accounts.txt and bank_account_transaction_file.txt)
qabank

# Phase 3 usage with explicit input and output files
qabank <input_accounts_file.txt> <output_transaction_file.atf>
```

## Input/Output (Phase 2)

### stdin Example
Example interactive input stream:

```text
login
admin
transfer
Bob Smith
22222
12345
9
logout
```

### stdout Example
Example console output for the above flow (colored based on urgency and to improve clarity):

```text
Welcome to the QA Bank System (qabank)
Type 'login' to begin session.
Enter session type (standard/admin):
Successfully logged in as an admin.
Enter source account holder name:
Enter source account number:
Enter destination account number:
Enter amount to transfer:
Transfer of $9.00 successful.
Successfully logged out.
```

### Input File Format (`bank_accounts.txt`)
Each account record is fixed length line of 37 characters (plus newline):

```text
NNNNN_AAAAAAAAAAAAAAAAAAAA_S_PPPPPPPP
```

- `NNNNN`: 5 digit account number, right justified with zeroes (e.g. 00023)
- `AAAAAAAAAAAAAAAAAAAA`: account holder name (20 characters max, left justified with spaces)
- `S`: status (active `A` or disabled `D`)
- `PPPPPPPP`: balance (8 characters max, e.g. `01000.00`)
- `_`: space for parsing

The bank accounts records file ends with a special bank account to demarcate the end of the file:

```text
00000 END_OF_FILE          A 00000.00
```

### Output File Format (`bank_account_transaction_file.txt`)
Each transaction record is formatted as:

```text
CC_AAAAAAAAAAAAAAAAAAAA_NNNNN_PPPPPPPP_MM
```

- `CC`: transaction code
- `AAAAAAAAAAAAAAAAAAAA`: account holder name (20 characters max, left justified with spaces)
- `NNNNN`: 5 digit account number, right justified with zeroes (e.g. 00023)
- `PPPPPPPP`: amount (`00000000` when amount is zero)
- `MM`: transaction-specific miscellaneous data
- `_`: space for parsing

Transaction codes used by Phase 2:

- `01`: Withdrawal
- `02`: Transfer
- `03`: Paybill
- `04`: Deposit
- `05`: Create
- `06`: Delete
- `07`: Disable
- `08`: ChangePlan
- `00`: End of Session

Paybill company codes:

- `EC`: The Bright Light Electric Company
- `CQ`: Credit Card Company
- `FI`: Fast Internet, Inc.

### Manual Testing
To test the application manually:
1.  Ensure a `bank_accounts.txt` file exists in your current directory.
    *   *Sample content:*
        ```text
        12345 John Doe             A 01000.00
        22222 Bob Smith            A 00010.00
        00000 END_OF_FILE          A 00000.00
        ```
2.  Run `qabank`.
3.  Type `login` to start a session.
4.  Type `help` to see available commands.

### Automated Testing (Phase 3)
In Phase 3, the testing infrastructure was expanded to validate the Front End against the Phase 1 test cases. We have specific scripts to automate execution and validation.

To run all test cases and generate the actual terminal and transaction outputs:
```bash
./run_tests.sh
```
*Note: This script reads all `.in.txt` files from `tests/test_inputs/` and deposits the results into `tests/actual_outputs/`.*

To validate the generated actual outputs against the expected outputs:
```bash
./validate_tests.sh
```
*Note: This script uses `diff` to compare the `.out` (terminal) and `.atf` (transaction) files in `tests/actual_outputs/` against the ground truth files in `tests/expected_outputs/`. It prints a PASS/FAIL report for each test.*

### 4. Commiting to GitHub repo
 - Please use your own branch and open a pull request into main
 - Each pull request will require a review from one of the other group members

 ```bash
 # Create your branch
 git checkout -b <yourname>-dev

 # Switch to a branch
 git switch <branch>
 ```
