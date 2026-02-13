import os
import glob
import subprocess
import pytest
import sys

# Define paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DIR = os.path.join(PROJECT_ROOT, "tests")
SRC_FILE = os.path.join(PROJECT_ROOT, "src", "front_end.py")

# Find all test cases (look for .in.txt files recursively)
# Returns a list of tuples: (test_name, input_file_path, expected_output_file_path)
def get_test_cases():
    test_files = glob.glob(os.path.join(TEST_DIR, "**", "*.in.txt"), recursive=True)
    test_cases = []
    for input_file in test_files:
        # Construct the expected output file path
        # Replaces .in.txt with .out.txt AND test_inputs with test_outputs
        expected_output_file = input_file.replace(".in.txt", ".out.txt").replace("test_inputs", "test_outputs")
        
        # Test name for pytest output (e.g., login/T01_login_standard)
        rel_path = os.path.relpath(input_file, TEST_DIR)
        test_name = os.path.splitext(os.path.splitext(rel_path)[0])[0]
        
        test_cases.append((test_name, input_file, expected_output_file))
    
    return test_cases

@pytest.mark.parametrize("test_name, input_file, expected_output_file", get_test_cases())
def test_cli_cases(test_name, input_file, expected_output_file):
    """
    Runs the CLI app with the given input file and asserts the transaction file output 
    matches the expected file.
    """
    # 1. Read input content
    with open(input_file, 'r') as f:
        input_data = f.read()

    # Ensure clean state (remove old output file if exists)
    output_filename = "bank_account_transaction_file.txt"
    if os.path.exists(output_filename):
        os.remove(output_filename)

    # 2. Run the application
    # Updated to run as module to handle imports correctly in the new structure
    process = subprocess.Popen(
        [sys.executable, "-m", "src.front_end.cli"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, # Capture stdout to keep console clean, but ignore it for comparison
        stderr=subprocess.PIPE,
        text=True,
        cwd=PROJECT_ROOT # Run from project root so paths work
    )

    stdout, stderr = process.communicate(input=input_data)

    # 3. Read Actual Output (from generated file)
    actual_output = ""
    if os.path.exists(output_filename):
        with open(output_filename, 'r') as f:
            actual_output = f.read()
    
    # 4. Read Expected Output
    if not os.path.exists(expected_output_file):
        pytest.fail(f"Expected output file not found: {expected_output_file}")

    with open(expected_output_file, 'r') as f:
        expected_output = f.read()

    # 5. Compare (Assertion)    
    # We strip whitespace from both ends to ignore trailing newlines differences
    
    # Determine if we should check transaction file or stdout based on expected output content
    import re
    is_transaction_file_expected = re.match(r'^\d{2}', expected_output)
    
    if is_transaction_file_expected:
        assert actual_output.strip() == expected_output.strip(), f"Transaction File mismatch for {test_name}.\n\nEXPECTED (File Content):\n{expected_output}\n\nACTUAL (File Content):\n{actual_output}\n\nAPP STDOUT:\n{stdout}\n\nAPP STDERR:\n{stderr}"
    else:
        # Assert that the expected output string appears in the stdout
        # Strip colour codes from stdout.
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_stdout = ansi_escape.sub('', stdout)
        
        # If expected is "Invalid Input...", check if it is in clean_stdout.
        assert expected_output.strip() in clean_stdout, f"STDOUT mismatch for {test_name}.\n\nEXPECTED (to be in stdout):\n{expected_output}\n\nACTUAL STDOUT (Cleaned):\n{clean_stdout}"
    
    # Cleanup
    if os.path.exists(output_filename):
        os.remove(output_filename)
