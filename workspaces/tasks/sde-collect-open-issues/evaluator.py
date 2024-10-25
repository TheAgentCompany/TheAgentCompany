import csv
import logging
import sys
import os

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

def grade_checkpoints(trajectory):
    checkpoints = [
        (lambda t: grade_checkpoint1(t), "http://the-agent-company.com:8929/root/sotopia/-/issues/ is in the trajectory"),
        (grade_checkpoint2, "/workspace/issues.csv has 12 lines and is a valid csv file"),
        (grade_checkpoint3, "/workspace/issues.csv contains line \"215,[FEAT]: Custom model docs\"")
    ]

    points = 0
    for grade_func, description in checkpoints:
        try:
            if callable(grade_func) and grade_func.__name__ == '<lambda>':
                passed = grade_func(trajectory)
            else:
                passed = grade_func()
            points += int(passed)
            print(f"{'✓' if passed else '✗'} {description}")
        except Exception as e:
            logging.warning(f"Error while grading checkpoint {description}: {e}")

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
        trajectory = []
    else:
        trajectory = load_trajectory(sys.argv[1])

    points = grade_checkpoints(trajectory)
    print(f"\nFinal points for Sotopia Issues task: {points}/3")