from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client, num_rocketchat_users_contacted, make_gitlab_request, grader
from config import GITLAB_USER

CHECKPOINT_1_POINTS = 2
CHECKPOINT_2_POINTS = 1
CHECKPOINT_3_POINTS = 2

rocket = create_rocketchat_client()

PROJECT_NAME = "risingwave"
PROJECT_PATH = f"{GITLAB_USER}/{PROJECT_NAME}"
ROCKETCHAT_USERNAMES = ["li_ming", "mike_chen", "mark_johnson"]
ISSUE_NAME = "Improve Logging for Bulk Request Failures"
MILESTONE_NAME = "release-1.9"
DESCRIPTION = "We need to improve the logging for bulk request failures, so we can better understand the root cause of the issue."
DUE_DATE = "2024-11-15"

issue = None

@grader
def grade_checkpoint1():
    return num_rocketchat_users_contacted(rocket, ROCKETCHAT_USERNAMES) == len(ROCKETCHAT_USERNAMES)

@grader
def grade_checkpoint2():
    response = make_gitlab_request(PROJECT_PATH, 'issues', params={'search': ISSUE_NAME})
    if response is None or response.status_code != 200:
        return False
    issues = response.json()
    for gitlab_issue in issues:
        if gitlab_issue['title'] == ISSUE_NAME:
            global issue
            issue = gitlab_issue
            return True
    return False

@grader
def grade_checkpoint3():
    global issue
    if issue is None:
        return False
    milestone = issue.get('milestone')
    milestone = milestone and milestone.get('title') == MILESTONE_NAME
    description = issue.get('description')
    description = description and DESCRIPTION in description
    due_date = issue.get('due_date')
    due_date = due_date and due_date == DUE_DATE

    return milestone and description and due_date

    
def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, CHECKPOINT_2_POINTS * int(passed2)))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(CHECKPOINT_3_POINTS, CHECKPOINT_3_POINTS * int(passed3)))
    return result
