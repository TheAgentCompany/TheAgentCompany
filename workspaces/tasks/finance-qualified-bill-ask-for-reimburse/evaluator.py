import os
import requests
from typing import List
from common import get_rocketchat_personal_chat_history
from scoring import Result, Checkpoint, bonus_for_completing_final

# Initialize RocketChat client
from common import create_rocketchat_client, grader
rocket = create_rocketchat_client()


@grader
def grade_checkpoint1(trajectory):
    return "dir=/Documents/Financials" in trajectory


@grader
def grade_checkpoint2(trajectory):
    return "dir=/Documents/Administrative%20Specialist" in trajectory



def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = grade_checkpoint2(trajectory)
    checkpoints.append(Checkpoint(1, int(passed2)))

    chat_history = get_rocketchat_personal_chat_history(rocket, "Mike Chen")
    passed3 = len(chat_history) > 0
    checkpoints.append(Checkpoint(1, int(passed3)))

    passed4 = "215" in ' '.join(chat_history)
    checkpoints.append(Checkpoint(2, 2 * int(passed4)))

    return result



