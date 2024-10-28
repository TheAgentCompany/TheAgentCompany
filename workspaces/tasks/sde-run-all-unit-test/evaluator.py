import logging
import re
import json
from typing import List

from scoring import Result, Checkpoint
from common import *

# Check if OpenHands repo is cloned
def grade_checkpoint1():
    return check_repo_exists('openhands')

# Check if at least one unit test is collected
def grade_checkpoint2(trajectory):
    try:
        match = re.search(r'collected (\d+) item(s)?', trajectory)
        if match: 
            return int(match.group(1)) > 0
        else:
            return False 
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint2: {e}")
        return False

# Check if at least one unit test passes
def grade_checkpoint3(trajectory):
    try:
        passed_match = re.search(r'(\d+) passed', trajectory)
        if passed_match:
            return int(passed_match.group(1)) > 0
        else:
            return False
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint3: {e}")
        return False

# Check if all unit tests pass
def grade_checkpoint4(trajectory):
    try:
        if 'failed' in trajectory.lower():
            return False
        
        collected_match = re.search(r'collected (\d+) item(s)?', trajectory)
        if not collected_match or int(collected_match.group(1)) == 0:
            return False
        
        passed_match = re.search(r'(\d+) passed', trajectory)
        if passed_match and collected_match:
            passed_tests = int(passed_match.group(1))
            total_tests = int(collected_match.group(1))
            return passed_tests == total_tests
        return False
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint4: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2(trajectory))))   
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3(trajectory))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint4(trajectory))))

    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))
