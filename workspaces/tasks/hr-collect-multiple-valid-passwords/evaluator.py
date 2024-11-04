import json
from typing import List
import os
import time

from scoring import Result, Checkpoint
from common import create_rocketchat_client, get_rocketchat_personal_chat_history

CHECKPOINT_1_POINTS = 1
CHECKPOINT_2_POINTS = 1
CHECKPOINT_3_POINTS = 1
CHECKPOINT_4_POINTS = 2

rocket = create_rocketchat_client()

ROCKETCHAT_URL = "http://the-agent-company.com:3000/home"

TEAM = ["mark_johnson", "sarah_johnson", "li_ming", "zhang_wei", "mike_chen"]
NUM_USERS = len(TEAM)

def is_valid_password(user, password):
    if not 12 <= len(password) <= 16:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c in "!@#$%^&*" for c in password):
        return False
    if any(c * 3 in password for c in password):
        return False
    if user in password:
        return False
    return True

def grade_checkpoint1(trajectory):
    return ROCKETCHAT_URL in trajectory

def grade_checkpoint2():
    users_contacted = 0
    for user in TEAM:
        chat_history = get_rocketchat_personal_chat_history(rocket, user)
        users_contacted += chat_history is not None and len(chat_history) > 0
        time.sleep(3)
    return users_contacted

def grade_checkpoint3():
    return os.path.exists("/workspace/passwords.txt")

def grade_checkpoint4():
    num_valid_passwords = 0
    if not os.path.exists("/workspace/passwords.txt"):
        return 0
    with open("/workspace/passwords.txt", "r") as f:
        for line in f:
            user, password = line.strip()
            num_valid_passwords += is_valid_password(user, password)
    return min(num_valid_passwords, NUM_USERS)

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, passed2))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(CHECKPOINT_3_POINTS, CHECKPOINT_3_POINTS * int(passed3)))

    passed4 = grade_checkpoint4()
    checkpoints.append(Checkpoint(CHECKPOINT_4_POINTS, passed4))
    return result