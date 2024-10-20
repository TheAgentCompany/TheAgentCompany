import json
import logging
import re
import sys
import os

# Check the repo has been cloned
def grade_checkpoint1():
    openhands_path = '/workspace/openhands'
    try:
        if not os.path.isdir(openhands_path):
            logging.warning("OpenHands directory not found")
            return False
        
        # Get all files in the directory
        files = os.listdir(openhands_path)
        
        # Check if there's at least one file
        if not files:
            logging.warning("No file found")
            return False
        
        instruction_file_path = os.path.join(openhands_path, ".openhands_instructions")
        return os.path.isfile(instruction_file_path)
    
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint1: {e}")
        return False

# Check it has test_agent_skill.py
def grade_checkpoint2():
    test_file_path = '/workspace/openhands/tests/unit/test_agent_skill.py'
    try:
        return os.path.isfile(test_file_path)
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint3: {e}")
        return False

# Check the file has unit test for open_file function
def grade_checkpoint3():
    test_file_path = '/workspace/openhands/tests/unit/test_agent_skill.py'
    try:
        with open(test_file_path, 'r') as file:
            content = file.read()
            return 'def test_open_file' in content
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint3: {e}")
        return False

# Check all the test passed
def grade_checkpoint4(trajectory):
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
        logging.warning(f"Error in grade_checkpoint4: {e}")
        return False

def grade_checkpoints(trajectory):
    checkpoints = [
        (grade_checkpoint1, "OpenHands code cloned in local workspace"),
        (grade_checkpoint2, "OpenHands/tests/unit/test_agent_skill.py exists"),
        (grade_checkpoint3, "There's a unit test for the function `open_file` in the unit test file"),
        (lambda: grade_checkpoint4(trajectory), "open_file function's unit tests are PASS in history")
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
    print(f"\nFinal points for OpenHands task: {points}/4")