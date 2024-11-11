from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client, get_rocketchat_personal_chat_history, make_gitlab_request, checkpoint
from config import GITLAB_USER

CHECKPOINT_1_POINTS = 1
CHECKPOINT_2_POINTS = 1
CHECKPOINT_3_POINTS = 1

rocket = create_rocketchat_client()

PROJECT_NAME = "risingwave"
PROJECT_PATH = f"{GITLAB_USER}/{PROJECT_NAME}"
ROCKETCHAT_USERNAME = "li_ming"
ISSUE_NAME = "Improve Logging for Bulk Request Failures"
MILESTONE_NAME = "release-1.9"

issue = None

@checkpoint
def grade_checkpoint1():
    chat_history = get_rocketchat_personal_chat_history(rocket, ROCKETCHAT_USERNAME)
    return chat_history is not None and len(chat_history) > 0

@checkpoint
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

@checkpoint
def grade_checkpoint3():
    global issue
    if issue is None:
        return False
    milestone = issue.get('milestone')
    return milestone and milestone['title'] == MILESTONE_NAME

    
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
