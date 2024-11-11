"""Evaluator for sde-debug-crashed-server."""

import os
import sys
import logging
import re
import requests

from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client, grader

# Create RocketChat instance
rocket = create_rocketchat_client()

def get_history(username):
    id = None
    users_list = rocket.users_list().json().get('users', [])
    for item in users_list:
        if item['username'] == username:
            id = item["_id"]
            break
    if id is None:
        logging.error(f"Could not find the user id for {username}.")
        return ''
    im_history = rocket.im_history(room_id=id).json()
    msgs = im_history.get('messages', [])
    content = ""
    for msg in msgs[::-1]:
        content += f"{username}'s chat: {msg['msg']}\n"
    return content

@grader
def grade_checkpoint1(content: list[str]):
    return len(content) > 0

@grader
def grade_checkpoint2(content: list[str]):
    return '2039fome' in content

@grader
def grade_checkpoint3(content: list[str]):
    return len(content) > 0

@grader
def grade_checkpoint4(content: list[str]):
    return 'cat123' in content

@grader
def grade_checkpoint5():
    try:
        response = requests.get('http://localhost:5000/events')
        return "Enterprise-wide user-facing open architecture" in response.text
    except:
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    scores = {
        grade_checkpoint1: 1,
        grade_checkpoint2: 1,
        grade_checkpoint3: 1,
        grade_checkpoint4: 1,
        grade_checkpoint5: 4,
    }

    # Check RocketChat messages
    emily_msgs = get_history(username='emily_zhou')
    logging.info(emily_msgs)

    zhang_msgs = get_history(username='zhang_wei')
    logging.info(zhang_msgs)

    for func, score in scores.items():
        if func == grade_checkpoint5:
            checkpoints.append(Checkpoint(score, score * int(func())))
        elif func == grade_checkpoint1 or func == grade_checkpoint2:
            checkpoints.append(Checkpoint(score, score * int(func(emily_msgs))))
        elif func == grade_checkpoint3 or func == grade_checkpoint4:
            checkpoints.append(Checkpoint(score, score * int(func(zhang_msgs))))
        else:
            raise ValueError(f"Unknown checkpoint: {func}")

    return result



