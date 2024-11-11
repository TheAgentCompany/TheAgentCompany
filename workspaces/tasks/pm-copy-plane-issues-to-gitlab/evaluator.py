import json
from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_any_of_given_checkpoints
from common import get_plane_project_id, make_gitlab_request, checkpoint
from config import GITLAB_USER

CHECKPOINT_1_POINTS = 1
CHECKPOINT_2_POINTS = 1
CHECKPOINT_3_POINTS = 1
CHECKPOINT_4_POINTS = 1

GITLAB_PROJECT_PATH = f"{GITLAB_USER}/janusgraph"

PROJECT_NAME = "JanusGraph"
PROJECT_ID = get_plane_project_id(PROJECT_NAME)
TODO_ISSUE_1 = "Integrate algorithms into existing graph database"
TODO_ISSUE_2 = "Implement optimization techniques for large datasets"
NEW_ISSUE_1 = "Research and design new algorithms"
NEW_ISSUE_2 = "Analyze current query performance bottlenecks"

def check_issue_exists_in_gitlab(issue_name):
    issues = make_gitlab_request(GITLAB_PROJECT_PATH, "issues")
    if issues is None:
        return False
    for issue in issues.json():
        if issue["title"] == issue_name:
            return True
    return False

@checkpoint
def grade_checkpoint1(trajectory):
    url = "tac/projects/f04e5c07-8fa2-4eaf-a35b-5cacf3f1d025/issues"
    return url in trajectory

@checkpoint
def grade_checkpoint2():
    return not check_issue_exists_in_gitlab(TODO_ISSUE_1) and not check_issue_exists_in_gitlab(TODO_ISSUE_2)

@checkpoint
def grade_checkpoint3():
    return check_issue_exists_in_gitlab(NEW_ISSUE_1)

@checkpoint
def grade_checkpoint4():
    return check_issue_exists_in_gitlab(NEW_ISSUE_2)

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any_of_given_checkpoints([3, 4]))
 
    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, CHECKPOINT_2_POINTS * int(passed2)))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(CHECKPOINT_3_POINTS, CHECKPOINT_3_POINTS * int(passed3)))

    passed4 = grade_checkpoint4()
    checkpoints.append(Checkpoint(CHECKPOINT_4_POINTS, CHECKPOINT_4_POINTS * int(passed4)))

    return result
