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

# Install dependencies
pip3 install -r requirements.txt
```

**Windows:**
```cmd
:: Create the virtual environment (one time only)
python -m venv sqa_final_project_venv

:: Activate the virtual environment
sqa_final_project_venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt
```

### 3. Running Tests
```bash
pytest
```

### 4. Commiting to GitHub repo
 - Please use your own branch and open a pull request into main
 - Each pull request will require a review from one of the other group members

 ```bash
 # Create your branch
 git checkout -b <yourname>-dev

 # Switch to a branch
 git switch <branch>
 ```