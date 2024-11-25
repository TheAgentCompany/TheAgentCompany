import os
import logging
import pandas as pd
from typing import List
from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client, evaluate_chat_history_with_llm, get_rocketchat_personal_chat_history, grader


# Create RocketChat instance
rocket = create_rocketchat_client()

# Reference solution
REFERENCE_DIRECTORY = "/workspace/signatories.csv"
REFERENCE_OWNCLOUD_PATH = "/Documents/Financials/Annual%20Reports"
REFERENCE_SIGNATORIES_COUNT = 27

def check_file_exists(file_path):
    abs_path = os.path.abspath(file_path)
    return os.path.isfile(abs_path)

@grader
def grade_checkpoint1():
    chat_history = get_rocketchat_personal_chat_history(rocket, "David Wong")
    return len(chat_history) > 0

@grader
def grade_checkpoint2(trajectory):
    # Confirm if the agent navigated to the correct directory
    return REFERENCE_OWNCLOUD_PATH in trajectory

@grader
def grade_checkpoint3():
    # Check for the existence of 'signatories.csv'
    return check_file_exists("/workspace/signatories.csv")

@grader
def grade_checkpoint4():
    # Validate the format and contents of 'signatories.csv'
    file_path = "/workspace/signatories.csv"
    if not check_file_exists(file_path):
        return False

    # Load the CSV
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower()

    # Required columns
    required_columns = ["name", "title", "date", "company"]
    if not all(col in df.columns for col in required_columns):
        logging.error(f"Missing required columns. Expected: {required_columns}")
        return False
    if len(df) != REFERENCE_SIGNATORIES_COUNT:
        logging.error(f"Row count mismatch. Expected: {REFERENCE_SIGNATORIES_COUNT}, Found: {len(df)}")
        return False

    # Ensure 'company' column only contains 'Amazon' or 'Alphabet'
    if not df['company'].isin(['Amazon', 'Alphabet']).all():
        logging.error("Invalid company names found.")
        return False

    # Validate the 'date' format (YYYY-MM-DD)
    try:
        pd.to_datetime(df['date'], format='%Y-%m-%d', errors='raise')
    except Exception as e:
        logging.error(f"Invalid date format in 'signature_date'. Expected YYYY-MM-DD. Error: {e}")
        return False

    # Ensure there are no duplicate rows
    if df.duplicated().any():
        logging.error("Duplicate rows found in the CSV.")
        return False

    # If all checks pass
    return True

@grader
def grade_checkpoint5():
    # Verify if Mark Johnson was contacted with the correct file path and signatories count
    predicate = f'The path file mentioned was {REFERENCE_DIRECTORY} and the number of signatories was {REFERENCE_SIGNATORIES_COUNT} '
    chat_history = evaluate_chat_history_with_llm(rocket, "Mark Johnson", predicate)
    
    return chat_history

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    
    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2(trajectory))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint4())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint5())))
    
    return result
