import os
import requests
from typing import List
from common import get_rocketchat_personal_chat_history
from scoring import Result, Checkpoint
from common import create_rocketchat_client, grader, evaluate_with_llm

# Initialize RocketChat client
rocket = create_rocketchat_client()

@grader
def grade_checkpoint1(trajectory):
    return "files/1447?dir=/Documents/Data%20Analysis" in trajectory

@grader
def grade_checkpoint_345(msg, keyword):
    return msg is not None and evaluate_with_llm(content=msg, predicate=f"the content contains `{keyword}`")

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
    checkpoints.append(Checkpoint(1, int(grade_checkpoint_345(msg, "male"))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint_345(msg, "married"))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint_345(msg, "french"))))
    
    # checkpoint 6
    passed6 = 0
    for msg in chat_history:
        segs = msg.lower().split("\n")
        if len(segs) >= 3:
            passed6 = grade_checkpoint_345(segs[0], "male") and grade_checkpoint_345(segs[1], "married") and grade_checkpoint_345(segs[2], "french")

    checkpoints.append(Checkpoint(1, int(passed6)))

    return result