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
    Runs the CLI app with the given input file and asserts the output matches the expected file.
    """
    # 1. Read input content
    with open(input_file, 'r') as f:
        input_data = f.read()

    # 2. Run the application
    # Updated to run as module to handle imports correctly in the new structure
    process = subprocess.Popen(
        [sys.executable, "-m", "src.front_end.cli"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=PROJECT_ROOT # Run from project root so paths work
    )

    stdout, stderr = process.communicate(input=input_data)

    # 3. Read expected output
    if not os.path.exists(expected_output_file):
        pytest.fail(f"Expected output file not found: {expected_output_file}")

    with open(expected_output_file, 'r') as f:
        expected_output = f.read()

    # 4. Compare (Assertion)    
    # Simple exact match for now:
    assert stdout == expected_output, f"Output mismatch for {test_name}.\n\nEXPECTED:\n{expected_output}\n\nACTUAL:\n{stdout}\n\nSTDERR:\n{stderr}"
