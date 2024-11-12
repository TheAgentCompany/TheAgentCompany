import os
import sys
import logging
import requests

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from config import *
from common import *

PLANE_PROJECT_ID = "73cb74f7-a7ac-4292-a915-e2f59a09a703"

# Check if OpenHands repo is cloned
@grader
def grade_checkpoint1():
    return check_repo_exists('openhands')

# Check if run unit test coverage command exists in trajectory
@grader
def grade_checkpoint2(trajectory):
    required_commands = ["poetry run pytest", "--cov=openhands"]
    return all(cmd in trajectory for cmd in required_commands)

# Check if coverage issue exists on Plane
@grader
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
@grader
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


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    checkpoints.append(Checkpoint(1, grade_checkpoint1()))
    checkpoints.append(Checkpoint(1, grade_checkpoint2(trajectory)))
    checkpoints.append(Checkpoint(1, grade_checkpoint3()))
    checkpoints.append(Checkpoint(1, grade_checkpoint4()))

    return result


