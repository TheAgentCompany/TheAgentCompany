import os
import requests
from typing import List
from common import get_rocketchat_personal_chat_history
from scoring import Result, Checkpoint
from common import create_rocketchat_client, grader

# Initialize RocketChat client
rocket = create_rocketchat_client()

@grader
def grade_checkpoint1(trajectory):
    return "apps/files/files/1447?dir=/Documents/Data%20Analysis" in trajectory


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # checkpoint 1
    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    # checkpoint 2
    chat_history = get_rocketchat_personal_chat_history(rocket, "Li Ming", content_only=True)
    passed2 = len(chat_history) > 0
    checkpoints.append(Checkpoint(1, int(passed2)))
    
    # checkpoint 3-5
    msg = "\n".join(chat_history).lower()
    passed3 = "male" in msg
    checkpoints.append(Checkpoint(1, int(passed3)))
    passed4 = "married" in msg
    checkpoints.append(Checkpoint(1, int(passed4)))
    passed5 = "french" in msg
    checkpoints.append(Checkpoint(1, int(passed5)))
    
    # checkpoint 6
    passed6 = 0
    for msg in chat_history:
        segs = msg.lower().split("\n")
        if len(segs) >= 3:
            if "male" in segs[0] and "married" in segs[1] and "french" in segs[2]:
                passed6 = 1

    checkpoints.append(Checkpoint(1, int(passed6)))

    return result