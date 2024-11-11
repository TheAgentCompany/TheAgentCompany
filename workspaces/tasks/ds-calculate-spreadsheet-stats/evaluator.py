import os
import re
from typing import List
from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client, get_rocketchat_personal_chat_history, checkpoint

# Initialize RocketChat client
rocket = create_rocketchat_client()

# Expected values for average row and column counts 
EXPECTED_AVG_ROWS = round(26.266666, 2)
EXPECTED_AVG_COLS = round(8.8, 2)

@grader
def grade_checkpoint1():
    """Check if '/workspace/data_stats.py' exists."""
    return os.path.exists("/workspace/data_stats.py")

def extract_reported_stats(message: str):
    """Extract reported row and column counts from the message, rounded to two decimal places."""
    row_match = re.search(r"average rows?: ([\d.]+)", message)
    col_match = re.search(r"average columns?: ([\d.]+)", message)

    if row_match and col_match:
        reported_rows = round(float(row_match.group(1)), 2)
        reported_columns = round(float(col_match.group(1)), 2)
        return reported_rows, reported_columns
    return None, None

@grader
def grade_checkpoint2():
    """Check if the reported average row and column counts are correct in RocketChat message."""
    chat_history = get_rocketchat_personal_chat_history(rocket, "jessica_lee")
    for message in chat_history:
        reported_rows, reported_columns = extract_reported_stats(message.lower())
        if (reported_rows == EXPECTED_AVG_ROWS and 
            reported_columns == EXPECTED_AVG_COLS):
            return True
    return False

@grader
def grade_checkpoint3():
    """Check if the agent informs Jessica Li with correct script path in RocketChat."""
    chat_history = get_rocketchat_personal_chat_history(rocket, "jessica_lee")
    for message in chat_history:
        if "analysis finished" in message.lower() and "/workspace/data_stats.py" in message:
            return True
    return False

def grade_checkpoints(trajectory=""):
    """Evaluate all checkpoints and return the results."""
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Checkpoint 1: Verify existence of data_stats.py
    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    # Checkpoint 2: Verify reported row/column counts in RocketChat message
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(3, 3 * int(passed2)))

    # Checkpoint 3: Verify conversation with Jessica Li regarding analysis completion and script path
    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(1, int(passed3)))

    return result
