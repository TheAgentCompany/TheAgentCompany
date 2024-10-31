import requests
import os
import json
from typing import List

from scoring import Result, Checkpoint
from common import get_plane_issue_details, get_plane_state_details, get_plane_issues_by_project_cycle, get_plane_cycle_details

CHECKPOINT_1_POINTS = 1
CHECKPOINT_2_POINTS = 1
CHECKPOINT_3_POINTS = 1
CHECKPOINT_4_POINTS = 2
CHECKPOINT_5_POINTS = 2

PROJECT_ID = "JANUS"
CYCLE_NAME = "Sprint 2"
ISSUE_1 = "Improve Logging for Bulk Request Failures"
ISSUE_2 = "Optimize Retry Mechanism for Out of Memory Errors"

def grade_checkpoint1(trajectory):
    url = "http://the-agent-company.com:8929/root/janusgraph/-/issues/4659"
    return url in trajectory

def grade_checkpoint2(trajectory):
    url = "http://the-agent-company.com:8929/root/janusgraph/-/issues/4660"
    return url in trajectory

def grade_checkpoint3(trajectory):
    url = "http://the-agent-company.com:8091/tac/projects/f04e5c07-8fa2-4eaf-a35b-5cacf3f1d025/issues/"
    return url in trajectory

def grade_checkpoint4():
    issue = get_plane_issue_details(PROJECT_ID, ISSUE_1)
    issue_id = issue["id"]
    cycle = get_plane_cycle_details(PROJECT_ID, CYCLE_NAME)
    print("cycle", cycle)
    issues_in_cycle = get_plane_issues_by_project_cycle(PROJECT_ID, cycle["id"])
    for issue in issues_in_cycle:
        if issue["id"] == issue_id:
            return True
    return False

def grade_checkpoint5():
    issue = get_plane_issue_details(PROJECT_ID, ISSUE_2)
    state = get_plane_state_details(PROJECT_ID, issue["state"])
    return state["name"] == "Done"
    


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


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))
