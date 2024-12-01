import os
import logging

from typing import List

from scoring import Result, Checkpoint
from common import evaluate_with_llm
from common import create_rocketchat_client, grader, get_rocketchat_personal_chat_history

# Create RocketChat instance
rocket = create_rocketchat_client()

@grader
def grade_checkpoint1():
    msgs = get_rocketchat_personal_chat_history(rocket, username)
    return len(msgs)>0


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Define the scores corresponding to when each function is True
    scores = {
        grade_checkpoint1: 1,
    }

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func())))

    return result



