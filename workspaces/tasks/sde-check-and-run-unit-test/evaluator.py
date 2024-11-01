import logging
import re

from typing import List

from scoring import Result, Checkpoint
from common import *

# Check the repo has been cloned
def grade_checkpoint1():
    return check_repo_exists('openhands')
    
# Check all the test passed
def grade_checkpoint2(trajectory):
    try:
        if 'test_open_file' not in trajectory:
            logging.warning("No test_open_file tests found in the trajectory")
            return False
        
        if 'failed' in trajectory.lower():
            logging.warning("Some tests failed")
            return False
        
        # Check if tests were selected and run
        selected_match = re.search(r'(\d+) selected', trajectory)
        if not selected_match or int(selected_match.group(1)) == 0:
            logging.warning("No tests were selected for open_file")
            return False
        
        return True
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint2: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = passed1 and grade_checkpoint2(trajectory)
    checkpoints.append(Checkpoint(1, int(passed2)))

    return result



