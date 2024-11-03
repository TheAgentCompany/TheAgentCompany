import json
from typing import List

from scoring import Result, Checkpoint
from common import get_plane_project_id, make_gitlab_request
from config import GITLAB_USER

CHECKPOINT_1_POINTS = 1
CHECKPOINT_2_POINTS = 1
CHECKPOINT_3_POINTS = 1
CHECKPOINT_4_POINTS = 2
CHECKPOINT_5_POINTS = 2

GITLAB_PROJECT_PATH = f"{GITLAB_USER}/openhands"

PROJECT_NAME = "OpenHands"
PROJECT_ID = get_plane_project_id(PROJECT_NAME)
ISSUE_1 = "Model: recall rate is 0"
ISSUE_2 = "Model: security problem"

def get_issue_url(issue_name):
    issues = make_gitlab_request(GITLAB_PROJECT_PATH, "issues", params={"search": issue_name})
    if issues is None:
        return None
    for issue in issues.json():
        if issue["title"] == issue_name:
            return issue["web_url"]

def grade_checkpoint1(trajectory):
    url = "tac/projects/73cb74f7-a7ac-4292-a915-e2f59a09a703/issues"
    return url in trajectory

def grade_checkpoint2(trajectory):
    url = get_issue_url(ISSUE_1)
    return url is not None and url in trajectory

def grade_checkpoint3(trajectory):
    url = get_issue_url(ISSUE_2)
    return url is not None and url in trajectory

def grade_checkpoint4():
    issues = make_gitlab_request(GITLAB_PROJECT_PATH, "issues", params={"search": ISSUE_1})
    if issues is None:
        return False
    for issue in issues.json():
        if issue["title"] == ISSUE_1:
            return issue["state"] == "opened"
    return False

def grade_checkpoint5():
    issues = make_gitlab_request(GITLAB_PROJECT_PATH, "issues", params={"search": ISSUE_2})
    if issues is None:
        return False
    for issue in issues.json():
        if issue["title"] == ISSUE_2:
            return issue["state"] == "closed"
    return False
    


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed1)))

    passed2 = grade_checkpoint2(trajectory)
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, CHECKPOINT_2_POINTS * int(passed2)))

    passed3 = grade_checkpoint3(trajectory)
    checkpoints.append(Checkpoint(CHECKPOINT_3_POINTS, CHECKPOINT_3_POINTS * int(passed3)))

    passed4 = grade_checkpoint4()
    checkpoints.append(Checkpoint(CHECKPOINT_4_POINTS, CHECKPOINT_4_POINTS * int(passed4)))

    passed5 = grade_checkpoint5()
    checkpoints.append(Checkpoint(CHECKPOINT_5_POINTS, CHECKPOINT_5_POINTS * int(passed5)))

    return result
