import os
import sys
import logging

from typing import List

from scoring import Result, Checkpoint
from common import evaluate_with_llm
from common import make_gitlab_request
from common import create_rocketchat_client, grader
from common import get_rocketchat_personal_chat_history, evaluate_chat_history_with_llm

# Create RocketChat instance
rocket = create_rocketchat_client()

# Configuration for gitlab
project_path = "root/openhands"
issue_id = 4158


def get_gitlab_issue_notes():
    try:
        response = make_gitlab_request(project_path, f"issues/{issue_id}/notes")
        return response.json()
    except Exception as e:
        logging.error(f"Error occurred while checking the repository: {e}")
        return []


@grader
def grade_checkpoint1(trajectory: str):
    return 'root/openhands/-/issues/4158' in trajectory


@grader
def grade_checkpoint2(username='Mike Chen'):
    msgs = get_rocketchat_personal_chat_history(rocket, username=username)
    return bool(msgs)


@grader
def grade_checkpoint3():
    issue_notes = get_gitlab_issue_notes()
    if issue_notes:
        return any(issue_note.get('id') not in [127283, 127284, 127285] for issue_note in issue_notes)
    else:
        return False

@grader
def grade_checkpoint4(username='Mike Chen'):

    issue_notes = get_gitlab_issue_notes()
    target = None
    if issue_notes:
        for issue_note in issue_notes:
            if issue_note.get('id') not in [127283, 127284, 127285]:
                target = issue_note.get('body')
    else:
        return False

    if target is None:
        return False

    return evaluate_chat_history_with_llm(rocket, username=username, predicate=target)


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))
    checkpoints.append(Checkpoint(2, 2 * int(grade_checkpoint4())))

    return result



