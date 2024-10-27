import os
import logging
import json
from typing import List

from scoring import Result, Checkpoint
from common import evaluate_with_llm
from common import create_rocketchat_client

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


def checkpoint1(username='jessica_lee'):
    msgs = get_history(username=username)
    return check_with_llm(msgs)

def checkpoint2(username='david_wong'):
    msgs = get_history(username=username)
    return check_with_llm(msgs)

def checkpoint3(username='huang_jie'):
    msgs = get_history(username=username)
    return check_with_llm(msgs)

def checkpoint4(username='mark_johnson'):
    msgs = get_history(username=username)
    return check_with_llm(msgs)


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Define the scores corresponding to when each function is True
    scores = {
        checkpoint1: 1,
        checkpoint2: 1,
        checkpoint3: 1,
        checkpoint4: 1,

    }

    for func, total_score in scores.items():
        checkpoints.append(total_score, total_score * int(func()))

    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))

