import json
from typing import List

from scoring import Result, Checkpoint
from common import get_plane_project_id, make_gitlab_request
from config import GITLAB_USER

CHECKPOINT_1_POINTS = 1
CHECKPOINT_2_POINTS = 2

GITLAB_PROJECT_PATH = f"{GITLAB_USER}/openhands"

PROJECT_NAME = "OpenHands"
PROJECT_ID = get_plane_project_id(PROJECT_NAME)
ISSUE_1 = "Model: recall rate is 0"
ISSUE_2 = "Model: security problem"

def grade_checkpoint1(trajectory):
    url = "tac/projects/73cb74f7-a7ac-4292-a915-e2f59a09a703/issues"
    return url in trajectory

def grade_checkpoint2():
    points = 0
    issues = make_gitlab_request(GITLAB_PROJECT_PATH, "issues", params={"search": ISSUE_1})
    if issues is not None:
        for issue in issues.json():
            if issue["title"] == ISSUE_1:
                points += issue["state"] == "opened"

    issues = make_gitlab_request(GITLAB_PROJECT_PATH, "issues", params={"search": ISSUE_2})
    if issues is not None:
        for issue in issues.json():
            if issue["title"] == ISSUE_2:
                points += issue["state"] == "closed"
    return points


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, passed2))
    return result
