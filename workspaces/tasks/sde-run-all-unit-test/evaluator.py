import json
import logging
import re
import sys

def load_trajectory(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.warning(f"Error reading trajectory file: {e}")
        return []

# Check if OpenHands repo is cloned
def grade_checkpoint1(trajectory):
    try:
        return any('git clone' in step.get('command', '') and 'openhands' in step.get('command', '').lower() for step in trajectory)
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint1: {e}")
        return False

# Check if at least one unit test is collected
def grade_checkpoint2(trajectory):
    try:
        pytest_output = next((step['output'] for step in trajectory if 'pytest' in step.get('command', '')), '')
        # Check the collected items is greater than 0
        match = re.search(r'collected (\d+) item(s)?', pytest_output)
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
        pytest_output = next((step['output'] for step in trajectory if 'pytest' in step.get('command', '')), '')
        passed_match = re.search(r'(\d+) passed', pytest_output)
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
        pytest_output = next((step['output'] for step in trajectory if 'pytest' in step.get('command', '')), '')
        if 'failed' in pytest_output.lower():
            return False
        
        collected_match = re.search(r'collected (\d+) item(s)?', pytest_output)
        if not collected_match or int(collected_match.group(1)) == 0:
            return False
        
        passed_match = re.search(r'(\d+) passed', pytest_output)
        if passed_match and collected_match:
            passed_tests = int(passed_match.group(1))
            total_tests = int(collected_match.group(1))
            return passed_tests == total_tests
        return False
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint4: {e}")
        return False

def grade_checkpoints(trajectory):
    checkpoints = [
        (grade_checkpoint1, "OpenHands repo is cloned"),
        (grade_checkpoint2, "At least one unit test is collected"),
        (grade_checkpoint3, "At least one unit test passes"),
        (grade_checkpoint4, "All unit tests pass")
    ]

    points = 0
    for grade_func, description in checkpoints:
        try:
            passed = grade_func(trajectory)
            points += int(passed)
            print(f"{'✓' if passed else '✗'} {description}")
            if not passed:
                break  
        except Exception as e:
            logging.warning(f"Error while grading checkpoint {description}: {e}")
            break  

    return points

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.warning("No trajectory file provided, assuming empty trajectory")
        trajectory = []
    else:
        trajectory = load_trajectory(sys.argv[1])

    points = grade_checkpoints(trajectory)
    print(f"\nFinal points for OpenHands task: {points}/4")