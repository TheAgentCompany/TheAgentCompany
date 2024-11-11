import json
from typing import List

from scoring import Result, Checkpoint
from common import get_plane_issue_details, get_plane_state_details, get_plane_issues_by_project_cycle, get_plane_cycle_details, get_plane_project_id, make_gitlab_request, checkpoint
from config import GITLAB_USER

CHECKPOINT_1_POINTS = 1
CHECKPOINT_2_POINTS = 1
CHECKPOINT_3_POINTS = 1
CHECKPOINT_4_POINTS = 2
CHECKPOINT_5_POINTS = 2

GITLAB_PROJECT_PATH = f"{GITLAB_USER}/janusgraph"

PROJECT_NAME = "JanusGraph"
PROJECT_ID = get_plane_project_id(PROJECT_NAME)
CYCLE_NAME = "Sprint 2"
ISSUE_1 = "Improve Logging for Bulk Request Failures"
ISSUE_2 = "Optimize Retry Mechanism for Out of Memory Errors"

def get_issue_url(issue_name):
    issues = make_gitlab_request(GITLAB_PROJECT_PATH, "issues", params={"search": issue_name})
    if issues is None:
        return None
    for issue in issues.json():
        if issue["title"] == issue_name:
            return issue["web_url"]

@checkpoint
def grade_checkpoint1(trajectory):
    url = get_issue_url(ISSUE_1)
    return url is not None and url in trajectory

@checkpoint
def grade_checkpoint2(trajectory):
    url = get_issue_url(ISSUE_2)
    return url is not None and url in trajectory

@checkpoint
def grade_checkpoint3(trajectory):
    url = "tac/projects/f04e5c07-8fa2-4eaf-a35b-5cacf3f1d025/issues"
    return url in trajectory

@checkpoint
def grade_checkpoint4():
    issue = get_plane_issue_details(PROJECT_ID, ISSUE_1)
    if issue is None:
        return False
    issue_id = issue["id"]
    cycle = get_plane_cycle_details(PROJECT_ID, CYCLE_NAME)
    if cycle is None:
        return False
    issues_in_cycle = get_plane_issues_by_project_cycle(PROJECT_ID, cycle["id"])
    if issues_in_cycle is None:
        return False
    for issue in issues_in_cycle:
        if issue["id"] == issue_id:
            return True
    return False

@checkpoint
def grade_checkpoint5():
    issue = get_plane_issue_details(PROJECT_ID, ISSUE_2)
    if issue is None:
        return False
    state = get_plane_state_details(PROJECT_ID, issue["state"])
    if state is None:
        return False
    return state["group"] == "completed"
    


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
