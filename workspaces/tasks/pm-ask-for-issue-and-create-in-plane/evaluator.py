from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client, get_rocketchat_personal_chat_history, get_plane_issue_details, get_plane_project_id, get_plane_cycle_details, get_plane_issues_by_project_cycle, create_plane_issue, add_plane_issue_to_cycle, grader

CHECKPOINT_1_POINTS = 1
CHECKPOINT_2_POINTS = 1
CHECKPOINT_3_POINTS = 1
CHECKPOINT_4_POINTS = 1

rocket = create_rocketchat_client()

PROJECT_NAME = "JanusGraph"
PROJECT_ID = get_plane_project_id(PROJECT_NAME)
ROCKETCHAT_USERNAME = "li_ming"
PLANE_USER_UUID = "9ccb0f88-b7af-4a68-91ca-624da7f307a6"
ISSUE_NAME = "Improve Logging for Bulk Request Failures"
CYCLE_NAME = "Sprint 2"

issue = None

@grader
def grade_checkpoint1():
    chat_history = get_rocketchat_personal_chat_history(rocket, ROCKETCHAT_USERNAME)
    return chat_history is not None and len(chat_history) > 0

@grader
def grade_checkpoint2():
    global issue
    issue = get_plane_issue_details(PROJECT_ID, ISSUE_NAME)
    return issue is not None

@grader
def grade_checkpoint3():
    global issue
    if issue is None:
        return False
    return PLANE_USER_UUID in issue["assignees"]

@grader
def grade_checkpoint4():
    global issue
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

    
def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, CHECKPOINT_2_POINTS * int(passed2)))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(CHECKPOINT_3_POINTS, CHECKPOINT_3_POINTS * int(passed3)))

    passed4 = grade_checkpoint4()
    checkpoints.append(Checkpoint(CHECKPOINT_4_POINTS, CHECKPOINT_4_POINTS * int(passed4)))
    return result
