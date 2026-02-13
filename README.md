# Software QA Final Project - Banking System

This project is a CLI-based Banking System developed for CSCI 3060U. It consists of a Front End (ATM) and Back End (Batch Processor), adhering to strict input/output constraints.

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

### 3. Usage (Phase 2 - Front End)

Once installed (via `pip install -e .`), you can run the application directly from your terminal:

```bash
qabank
```

#### Manual Testing
To test the application manually:
1.  Ensure a `bank_accounts.txt` file exists in your current directory.
    *   *Sample content:*
        ```text
        12345 User Name            A 00500.00
        99999 Admin User           A 00000.00
        00000 END_OF_FILE          A 00000.00
        ```
2.  Run `qabank`.
3.  Type `login` to start a session.
4.  Type `help` to see available commands.

#### Automated Testing / Demonstration
To run all test cases from Phase 1 against the current build and see the output in the console:

```bash
./run_all_tests.sh
```
*Note: This script runs the application against all `.in.txt` files in `tests/test_inputs/` sequentially. It is useful for verifying that the application handles all input scenarios without crashing.*

To run the formal test suite (verification against expected output):
```bash
pytest
```
*(Note: `pytest` will currently fail because the UI output prompts (e.g., "Welcome...") do not match the strict Phase 1 output files which expect only transaction logs.)*

### 4. Commiting to GitHub repo
 - Please use your own branch and open a pull request into main
 - Each pull request will require a review from one of the other group members

 ```bash
 # Create your branch
 git checkout -b <yourname>-dev

 # Switch to a branch
 git switch <branch>
 ```