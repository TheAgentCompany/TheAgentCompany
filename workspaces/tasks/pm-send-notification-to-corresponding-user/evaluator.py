import os
import logging

from typing import List

from scoring import Result, Checkpoint
from common import evaluate_with_llm
from common import create_rocketchat_client, grader

# Create RocketChat instance
rocket = create_rocketchat_client()


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

def check_with_llm(msgs):
    content = ""
    for msg in msgs[::-1]:
        content += msg['msg']

    if len(content)==0:
        return False

    predicate = 'there is a plan to hold a kickoff meeting for the main Q4 project'
    return evaluate_with_llm(content, predicate)


@grader
def grade_checkpoint1(username='jessica_lee'):
    msgs = get_history(username=username)
    return check_with_llm(msgs)

@grader
def grade_checkpoint2(username='david_wong'):
    msgs = get_history(username=username)
    return check_with_llm(msgs)

@grader
def grade_checkpoint3(username='huang_jie'):
    msgs = get_history(username=username)
    return check_with_llm(msgs)

@grader
def grade_checkpoint4(username='mark_johnson'):
    msgs = get_history(username=username)
    return check_with_llm(msgs)


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Define the scores corresponding to when each function is True
    scores = {
        grade_checkpoint1: 1,
        grade_checkpoint2: 1,
        grade_checkpoint3: 1,
        grade_checkpoint4: 1,

    }

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func())))

    return result




