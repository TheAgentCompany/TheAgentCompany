import logging
import re
import sys
import os
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

def grade_checkpoints(trajectory):
    checkpoints = [
        (grade_checkpoint1, "OpenHands code cloned in local workspace"),
        (lambda: grade_checkpoint2(trajectory), "open_file function's unit tests are PASS in history")
    ]

    points = 0
    for grade_func, description in checkpoints:
        try:
            passed = grade_func()
            points += int(passed)
            print(f"{'✓' if passed else '✗'} {description}")
            if not passed:
                break  
        except Exception as e:
            logging.warning(f"Error while grading checkpoint {description}: {e}")
            break 

    return points

def load_trajectory(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except Exception as e:
        logging.warning(f"Error reading trajectory file: {e}")
        return ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.warning("No trajectory file provided, assuming empty trajectory")
        trajectory = ""
    else:
        trajectory = load_trajectory(sys.argv[1])

    points = grade_checkpoints(trajectory)
    print(f"\nFinal points for OpenHands task: {points}/2")