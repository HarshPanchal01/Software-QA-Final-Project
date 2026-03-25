import pytest
from unittest.mock import patch

from src.back_end.fee_calculator import FeeCalculator
from src.shared.bank_accounts import AccountPlan
from src.back_end.merged_transactions import MergedTransactions



"""
    Statement Coverage Unit Test Cases
    Method: FeeCalculator.calculate(plan: AccountPlan) -> float
"""

def test_FeeCalculator_calculate_student_plan() -> None:
    """Test Case ID: SC1"""
    fee = FeeCalculator.calculate(AccountPlan.STUDENT)
    assert fee == 0.05

def test_FeeCalculator_calculate_non_student_plan() -> None:
    """Test Case ID: SC2"""
    fee = FeeCalculator.calculate(AccountPlan.NON_STUDENT)
    assert fee == 0.10

def test_FeeCalculator_calculate_unknown_plan() -> None:
    """Test Case ID: SC3"""
    fee = FeeCalculator.calculate(AccountPlan.UNKNOWN)
    assert fee == 0.00



"""
    Decision and Loop Coverage Unit Test Cases
    Method: MergedTransactions.merge_transactions(file_path: str) -> None
"""

@pytest.fixture
def mock_new_transactions_dir(tmp_path) -> None:
    """Fixture to mock NEW_TRANSACTIONS_DIR with a temporary directory."""
    new_dir = tmp_path / "new"
    new_dir.mkdir()
    # Need to patch the value where it is used in the module
    with patch("src.back_end.merged_transactions.NEW_TRANSACTIONS_DIR", str(new_dir) + "/"):
        yield new_dir


def test_merge_transactions_empty_directory(mock_new_transactions_dir, tmp_path) -> None:
    """
    Test Case ID: DL1
    Inputs: Directory exists but contains no .txt files
    Expected: Merged file created with only EOF record
    """
    output_file = tmp_path / "merged.txt"
    MergedTransactions.merge_transactions(str(output_file))
    
    assert output_file.exists()
    content = output_file.read_text()
    assert content == "00                      00000 00000000   \n"


def test_merge_transactions_one_valid_no_eof(mock_new_transactions_dir, tmp_path) -> None:
    """
    Test Case ID: DL2
    Inputs: One .txt file, one valid transaction, no EOF
    Expected: Transaction written, file not deleted, EOF appended
    """
    input_file = mock_new_transactions_dir / "1.txt"
    input_file.write_text("01 John Doe             12345 00050.00   \n")
    
    output_file = tmp_path / "merged.txt"
    MergedTransactions.merge_transactions(str(output_file))
    
    assert output_file.exists()
    content = output_file.read_text().splitlines()
    assert len(content) == 2
    assert content[0] == "01 John Doe             12345 00050.00   "
    assert content[1] == "00                      00000 00000000   "
    
    # File should not be deleted because there was no EOF marker
    assert input_file.exists()


def test_merge_transactions_one_file_first_line_eof(mock_new_transactions_dir, tmp_path) -> None:
    """
    Test Case ID: DL3
    Inputs: One .txt file, first line is EOF
    Expected: No transaction written, file deleted, EOF appended
    """
    input_file = mock_new_transactions_dir / "1.txt"
    input_file.write_text("00 John Doe             12345 00050.00   \n01 John Doe             12345 00050.00   \n")
    
    output_file = tmp_path / "merged.txt"
    MergedTransactions.merge_transactions(str(output_file))
    
    assert output_file.exists()
    content = output_file.read_text()
    assert content == "00                      00000 00000000   \n"
    
    # File should be deleted because an EOF marker was read
    assert not input_file.exists()


def test_merge_transactions_one_file_multiple_then_eof(mock_new_transactions_dir, tmp_path) -> None:
    """
    Test Case ID: DL4
    Inputs: One .txt file, multiple transactions then EOF
    Expected: All valid lines written until EOF, file deleted
    """
    input_file = mock_new_transactions_dir / "1.txt"
    input_file.write_text("01 John Doe             12345 00050.00   \n02 John Doe             12345 00050.00   \n00 John Doe             00000 00000000   \n")
    
    output_file = tmp_path / "merged.txt"
    MergedTransactions.merge_transactions(str(output_file))
    
    assert output_file.exists()
    content = output_file.read_text().splitlines()
    assert len(content) == 3
    assert content[0] == "01 John Doe             12345 00050.00   "
    assert content[1] == "02 John Doe             12345 00050.00   "
    assert content[2] == "00                      00000 00000000   "
    
    assert not input_file.exists()


def test_merge_transactions_multiple_files_valid(mock_new_transactions_dir, tmp_path) -> None:
    """
    Test Case ID: DL5
    Inputs: Multiple .txt files with valid transactions
    Expected: All files merged in order, EOF appended
    """
    input_file1 = mock_new_transactions_dir / "1.txt"
    input_file1.write_text("01 John Doe             12345 00050.00   \n00 John Doe             00000 00000000   \n")
    
    input_file2 = mock_new_transactions_dir / "2.txt"
    input_file2.write_text("02 John Doe             12345 00050.00   \n00 John Doe             00000 00000000   \n")
    
    output_file = tmp_path / "merged.txt"
    MergedTransactions.merge_transactions(str(output_file))
    
    assert output_file.exists()
    content = output_file.read_text().splitlines()
    assert len(content) == 3
    assert content[0] == "01 John Doe             12345 00050.00   "
    assert content[1] == "02 John Doe             12345 00050.00   "
    assert content[2] == "00                      00000 00000000   "
    
    assert not input_file1.exists()
    assert not input_file2.exists()


def test_merge_transactions_one_file_no_eof_line(mock_new_transactions_dir, tmp_path) -> None:
    """
    Test Case ID: DL6
    Inputs: One .txt file with no EOF line
    Expected: All lines written, file not deleted
    """
    input_file = mock_new_transactions_dir / "1.txt"
    input_file.write_text("01 John Doe             12345 00050.00   \n02 John Doe             12345 00050.00   \n")
    
    output_file = tmp_path / "merged.txt"
    MergedTransactions.merge_transactions(str(output_file))
    
    assert output_file.exists()
    content = output_file.read_text().splitlines()
    assert len(content) == 3
    assert content[0] == "01 John Doe             12345 00050.00   "
    assert content[1] == "02 John Doe             12345 00050.00   "
    assert content[2] == "00                      00000 00000000   "
    
    assert input_file.exists()


def test_merge_transactions_empty_txt_file(mock_new_transactions_dir, tmp_path) -> None:
    """
    Test Case ID: DL7
    Inputs: One empty .txt file
    Expected: Nothing written except final EOF, file not deleted
    """
    input_file = mock_new_transactions_dir / "1.txt"
    input_file.write_text("")
    
    output_file = tmp_path / "merged.txt"
    MergedTransactions.merge_transactions(str(output_file))
    
    assert output_file.exists()
    content = output_file.read_text()
    assert content == "00                      00000 00000000   \n"
    
    assert input_file.exists()


def test_merge_transactions_non_txt_files(mock_new_transactions_dir, tmp_path) -> None:
    """
    Test Case ID: DL8
    Inputs: Directory contains non .txt files
    Expected: Non .txt files ignored, only EOF appended
    """
    input_file = mock_new_transactions_dir / "1.log"
    input_file.write_text("01 John Doe             12345 00050.00   \n")
    
    output_file = tmp_path / "merged.txt"
    MergedTransactions.merge_transactions(str(output_file))
    
    assert output_file.exists()
    content = output_file.read_text()
    assert content == "00                      00000 00000000   \n"
    
    assert input_file.exists()


def test_merge_transactions_invalid_file_path(mock_new_transactions_dir, tmp_path, capsys) -> None:
    """
    Test Case ID: DL9
    Inputs: Invalid file path
    Expected: Error message printed, function exits safely
    """
    # Create a directory named 1.txt to trigger an error when it tries to open it as a file
    input_file = mock_new_transactions_dir / "1.txt"
    input_file.mkdir()
    
    output_file = tmp_path / "merged.txt"
    MergedTransactions.merge_transactions(str(output_file))
    
    captured = capsys.readouterr()
    assert "ERROR: Unexpected error while merging transactions" in captured.out
