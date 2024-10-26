import os
import sys
import logging
import requests
from config import *
from common import *

PLANE_PROJECT_ID = "73cb74f7-a7ac-4292-a915-e2f59a09a703"

# Check if OpenHands repo is cloned
def grade_checkpoint1():
    return check_repo_exists('openhands')

# Check if run unit test coverage command exists in trajectory
def grade_checkpoint2(trajectory):
    required_commands = ["poetry run pytest", "--cov=openhands"]
    return all(cmd in trajectory for cmd in required_commands)

# Check if coverage issue exists on Plane
def grade_checkpoint3():
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{PLANE_PROJECT_ID}/issues/"
    
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        if response.status_code == 200:
            issues = response.json().get("results", [])
            for issue in issues:
                if "unit test coverage" in issue.get('name', '').lower():
                    return True
        return False
    except Exception as e:
        logging.warning(f"Error checking Plane issues: {e}")
        return False

# Check if coverage number in issue is correct
def grade_checkpoint4():
    EXPECTED_COVERAGE = 55.65 
    
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{PLANE_PROJECT_ID}/issues/"
    
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        if response.status_code == 200:
            issues = response.json().get("results", [])
            for issue in issues:
                if "unit test coverage" in issue.get('name', '').lower():
                    issue_text = issue.get('name', '')
                    try:
                        coverage_str = issue_text.split('%')[0].split()[-1]
                        reported_coverage = float(coverage_str)
                        
                        return abs(reported_coverage - EXPECTED_COVERAGE) <= 1
                    except Exception as e:
                        logging.warning(f"Error extract the coverage rate: {e}")
                        return False
        return False
    except Exception as e:
        logging.warning(f"Error checking coverage in issues: {e}")
        return False

def grade_checkpoints(trajectory):
    checkpoints = [
        (grade_checkpoint1, "OpenHands code cloned in local workspace"),
        (lambda: grade_checkpoint2(trajectory), "Command about running unit test coverage in agent trajectory"),
        (grade_checkpoint3, "Post about unit test coverage exists on Plane"),
        (grade_checkpoint4, "Post contains the correct unit test coverage number")
    ]
    
    points = 0
    for i, (grade_func, description) in enumerate(checkpoints):
        try:
            passed = grade_func(trajectory) if grade_func == grade_checkpoint2 else grade_func()
            if passed:
                if i == 3:  
                    points = 4 
                else:
                    points += 1
            print(f"{'✓' if passed else '✗'} {description}")
        except Exception as e:
            logging.warning(f"Error while grading checkpoint {description}: {e}")
            break
    
    return points

def load_trajectory(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
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
    print(f"\nFinal points: {points}/4")