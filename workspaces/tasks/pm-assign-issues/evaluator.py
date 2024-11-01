import requests
import logging

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import get_plane_project_id, get_plane_project_all_issues
from config import *


############################# Helper Functions #####################################


PROJECT_NAME = "Backend Development"
USERS = ["emilyzhou", "alexturner", "emmalewis"]
#mapped uuid of the users to issues
ISSUES = {
    "8e15a7e6-635a-4ca9-a273-eb1c7a692c23": "Implement new navigation bar for the frontend",
    "2148bd98-f9e6-4637-848b-62bc6a63b675": "Set up backend API for payment processing",
    "c8c76e66-f8b2-4b58-9a9c-d779b60b8d15": "Write unit tests for authentication service"
}

def grade_checkpoint1():
    """Verify the project creation."""
    return get_plane_project_id(PROJECT_NAME) is not None


def check_issue_present(project_id, issue_text):
    """Check if a specific issue is present in the project by title."""
    issues = get_plane_project_all_issues(project_id)
    for issue in issues:
        if issue.get('name') == issue_text:
            logging.info(f"Issue '{issue_text}' found in project.")
            return True
    logging.warning(f"Issue '{issue_text}' not found in project.")
    return False

def check_issue_assigned(project_id, issue_text, assignee):
    """Check if the issue is assigned to the correct participant."""
    issues = get_plane_project_all_issues(project_id)
    for issue in issues:
        if issue.get('name') == issue_text:
            assignees = issue.get('assignees', [])
            if assignee in assignees:
                logging.info(f"Issue '{issue_text}' is assigned to '{assignee}'.")
                return True
            else:
                logging.warning(f"Issue '{issue_text}' is not assigned to '{assignee}'. Assigned to: {assignees}")
                return False
    logging.warning(f"Issue '{issue_text}' not found in project.")
    return False

def grade_checkpoint2(trajectory):
    """Check if part of the project URL is accessed in the trajectory."""
    target_substring = "/settings/members"
    return target_substring in trajectory

def grade_checkpoint3():
    """Verify all issues with correct titles are present in the project."""
    project_id = get_plane_project_id(PROJECT_NAME)
    if project_id:
        # Check for the presence of each issue title
        issue_presence_checks = [
            check_issue_present(project_id, title)
            for title in ISSUES.values()
        ]
        return all(issue_presence_checks)
    return False

def grade_checkpoint_final():
    """Verify all issues are assigned correctly to the specified users."""
    project_id = get_plane_project_id(PROJECT_NAME)
    if project_id:
        # Check for correct assignments of each issue
        issue_assignment_checks = [
            check_issue_assigned(project_id, title, assignee)
            for assignee, title in ISSUES.items()
        ]
        return all(issue_assignment_checks)
    return False

############################# Evaluator #####################################

def grade_checkpoints(trajectory):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    # Checkpoint 1: Project creation
    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(total=1, result=int(passed1)))

    passed2 = grade_checkpoint2(trajectory)
    checkpoints.append(Checkpoint(total=1, result=int(passed2)))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(total=1, result=int(passed3)))

    # Final checkpoint: Issues assigned correctly
    passed_final = grade_checkpoint_final()
    checkpoints.append(Checkpoint(total=2, result=int(passed_final) * 2))

    return result



