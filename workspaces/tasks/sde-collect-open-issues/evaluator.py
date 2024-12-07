import csv
import logging
import sys
import os

from typing import List

from scoring import Result, Checkpoint
from common import grader

def is_valid_csv(file_path):
    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            # Check if the file is empty
            if not next(reader, None):
                return False
            # Iterate through the remaining rows to check for any errors
            for row in reader:
                pass
        return True
    except Exception:
        return False


# Check http://the-agent-company.com:8929/root/sotopia/-/issues is in the trajectory
@grader
def grade_checkpoint1(trajectory):
    target_url = "http://the-agent-company.com:8929/root/sotopia/-/issues"
    
    try:
        return target_url in (str(trajectory))
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint1: {e}")
        return False

# Check /workspace/issues.csv has 12 lines and is a valid csv file
@grader
def grade_checkpoint2():
    try:
        file_path = '/workspace/issues.csv'
        is_valid =  is_valid_csv(file_path)
        if not is_valid:
            return False
        with open(file_path, 'r') as file:
            lines = file.readlines()
            lines = [line for line in lines if "," in line]
            if len(lines) != 13:
                return False
        return True
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint2: {e}")
        return False

# Check /workspace/issues.csv contains line “215,[FEAT]: Custom model docs”
@grader
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



