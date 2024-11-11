import re
from typing import List
from scoring import Result, Checkpoint, bonus_for_completing_any
from common import create_rocketchat_client, get_rocketchat_personal_chat_history, grader

# Create RocketChat instance
rocket = create_rocketchat_client()

# Expected results for the problematic files
EXPECTED_MEANINGLESS_NAMES = ["wrgbn i53b;6.xlsx"]
EXPECTED_NUMERIC_NAMES = ["12.xlsx", "28.xlsx", "1111111.xlsx"]
EXPECTED_UNUSUAL_CHAR_NAMES = ["Under~Reporters.xlsx", "wrgbn i53b;6.xlsx"]

# URL that should be accessed for Checkpoint 1
DATA_ANALYSIS_FOLDER_URL = "/Documents/Data%20Analysis"


@grader
def grade_checkpoint1(trajectory: str) -> bool:
    """Check if the agent visits the "Data Analysis" folder."""
    return DATA_ANALYSIS_FOLDER_URL in trajectory


@grader
def grade_checkpoint2() -> bool:
    """Check if the agent reports to Jessica Lee on RocketChat."""
    messages = get_rocketchat_personal_chat_history(rocket, "jessica_lee")
    return bool(messages)  # True if there is at least one message


@grader
def grade_checkpoint3() -> bool:
    """Check if the agent identifies files without meaningful names correctly in the report to Jessica Lee."""
    messages = get_rocketchat_personal_chat_history(rocket, "jessica_lee")
    if not messages:
        return False

    # Check if the message contains the correct list of files without meaningful names
    for msg in messages:
        message_text = msg.lower()
        meaningless_section = re.search(r'files without meaningful names: (.+)', message_text)
        if meaningless_section:
            reported_meaningless_names = meaningless_section.group(1).split(", ")
            if sorted(reported_meaningless_names) == sorted([name.lower() for name in EXPECTED_MEANINGLESS_NAMES]):
                return True

    return False


@grader
def grade_checkpoint4() -> bool:
    """Check if the agent identifies files with all numeric names correctly in the report to Jessica Lee."""
    messages = get_rocketchat_personal_chat_history(rocket, "jessica_lee")
    if not messages:
        return False

    # Check if the message contains the correct list of numeric file names
    for msg in messages:
        message_text = msg.lower()
        numeric_section = re.search(r"files with all numerical names: (.+)", message_text)
        if numeric_section:
            reported_numeric_names = numeric_section.group(1).split(", ")
            if sorted(reported_numeric_names) == sorted([name.lower() for name in EXPECTED_NUMERIC_NAMES]):
                return True

    return False


@grader
def grade_checkpoint5() -> bool:
    """Check if the agent identifies files with unusual characters correctly in the report to Jessica Lee."""
    messages = get_rocketchat_personal_chat_history(rocket, "jessica_lee")
    if not messages:
        return False

    # Check if the message contains the correct list of unusual character file names
    for msg in messages:
        message_text = msg.lower()
        unusual_section = re.search(r"files with unusual characters: (.+)", message_text)
        if unusual_section:
            reported_unusual_names = unusual_section.group(1).split(", ")
            if sorted(reported_unusual_names) == sorted([name.lower() for name in EXPECTED_UNUSUAL_CHAR_NAMES]):
                return True

    return False


def grade_checkpoints(trajectory="") -> Result:
    """
    Evaluate all checkpoints and return the results.
    """
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any)

   # Checkpoint 1: Check if the agent visits the "Data Analysis" folder
    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    # Checkpoint 2: Check if the agent reports to Jessica Lee 
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    # Checkpoint 3: Check if files without meaningful names are correctly identified in the report
    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(1, int(passed3)))

    # Checkpoint 4: Check if files with all numeric names are correctly identified in the report
    passed4 = grade_checkpoint4()
    checkpoints.append(Checkpoint(1, int(passed4)))

    # Checkpoint 5: Check if files with unusual characters are correctly identified in the report
    passed5 = grade_checkpoint5()
    checkpoints.append(Checkpoint(1, int(passed5)))

    return result
