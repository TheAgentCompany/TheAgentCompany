import os
import sys
import logging

from typing import List

from scoring import Result, Checkpoint
from common import evaluate_with_llm
from common import make_gitlab_request
from common import create_rocketchat_client, checkpoint

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

def get_history(username):
    id = ""
    for item in rocket.users_list().json()['users']:
        if item['username'] == username:
            id = item["_id"]
            break
    msgs = rocket.im_history(room_id=id).json()['messages']

    for msg in msgs[::-1]:
        print(f"{username}'s chat: {msg['msg']}")

    return msgs


def check_with_llm(msgs, predicate):
    content = ""
    for msg in msgs[::-1]:
        content += msg['msg']

    if len(content) == 0:
        return False

    return evaluate_with_llm(content, predicate)


@checkpoint
def grade_checkpoint1(url='http://the-agent-company.com:8929/root/openhands/-/issues/4158'):
    if len(sys.argv) < 2:
        trajectory = ""
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                trajectory = file.read()
        except Exception as e:
            print(f"Error reading trajectory file: {e}")
            exit(1)
    return url in trajectory


@checkpoint
def grade_checkpoint2(username='mike_chen'):
    msgs = get_history(username=username)
    return bool(msgs)


@checkpoint
def grade_checkpoint3():
    issue_notes = get_gitlab_issue_notes()
    if issue_notes:
        return any(issue_note.get('id') not in [127283, 127284, 127285] for issue_note in issue_notes)
    else:
        return False

@checkpoint
def grade_checkpoint4(username='mike_chen'):
    msgs = get_history(username=username)

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

    return check_with_llm(msgs, predicate=target)


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Define the scores corresponding to when each function is True
    scores = {
        grade_checkpoint1: 1,
        grade_checkpoint2: 1,
        grade_checkpoint3: 1,
        grade_checkpoint4: 2,

    }

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func())))

    return result



