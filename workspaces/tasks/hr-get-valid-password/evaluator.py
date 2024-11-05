import json
from typing import List
import os

from scoring import Result, Checkpoint
from common import create_rocketchat_client, get_rocketchat_personal_chat_history

CHECKPOINT_1_POINTS = 1
CHECKPOINT_2_POINTS = 1
CHECKPOINT_3_POINTS = 2

rocket = create_rocketchat_client()

ROCKETCHAT_URL = "http://the-agent-company.com:3000/home"

USERNAME = "mark_johnson"
VALID_PASSWORD = "Fl0w3r#Br1ght"

def grade_checkpoint1():
    chat_history = get_rocketchat_personal_chat_history(rocket, "mark_johnson")
    return chat_history is not None and len(chat_history) > 0

def grade_checkpoint2():
    return os.path.exists("/workspace/password.txt")

def grade_checkpoint3():
    if not os.path.exists("/workspace/password.txt"):
        return False
    with open("/workspace/password.txt", "r") as f:
        password = f.read().strip()

    return password == VALID_PASSWORD
    
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
