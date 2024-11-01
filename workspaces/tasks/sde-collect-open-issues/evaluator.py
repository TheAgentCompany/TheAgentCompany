import csv
import logging
import sys
import os

from typing import List

from scoring import Result, Checkpoint

# Check http://the-agent-company.com:8929/root/sotopia/-/issues is in the trajectory
def grade_checkpoint1(trajectory):
    target_url = "http://the-agent-company.com:8929/root/sotopia/-/issues"
    
    try:
        return target_url in (str(trajectory))
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint1: {e}")
        return False

# Check /workspace/issues.csv has 12 lines and is a valid csv file
def grade_checkpoint2():
    try:
        file_path = '/workspace/issues.csv'
        if not os.path.isfile(file_path):
            return False
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) != 12:
                return False
            for line in lines:
                if ',' not in line:
                    return False
        return True
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint2: {e}")
        return False

# Check /workspace/issues.csv contains line “215,[FEAT]: Custom model docs”
def grade_checkpoint3():
    try:
        file_path = '/workspace/issues.csv'
        target_line = "215,[FEAT]: Custom model docs"
        with open(file_path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if len(row) == 2 and row[0] == "215" and row[1] == "[FEAT]: Custom model docs":
                    return True
        return False
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint3: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    grading_functions = [
        (lambda t: grade_checkpoint1(t), "http://the-agent-company.com:8929/root/sotopia/-/issues/ is in the trajectory"),
        (grade_checkpoint2, "/workspace/issues.csv has 12 lines and is a valid csv file"),
        (grade_checkpoint3, "/workspace/issues.csv contains line \"215,[FEAT]: Custom model docs\"")
    ]

    for grade_func, description in grading_functions:
        try:
            if callable(grade_func) and grade_func.__name__ == '<lambda>':
                passed = grade_func(trajectory)
            else:
                passed = grade_func()
            logging.info(f"{'✓' if passed else '✗'} {description}")
            checkpoints.append(Checkpoint(1, int(passed)))
        except Exception as e:
            logging.warning(f"Error while grading checkpoint {description}: {e}")

    return result



