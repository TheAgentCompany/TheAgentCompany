import requests
import os

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import grader


@grader
def grade_checkpoint1(trajectory):
    policy_file_path = "dir=/Documents/Administrative%20Specialist"
    return policy_file_path in trajectory

@grader
def grade_checkpoint2():
    path = "/workspace/reimburse.txt"
    if not os.path.exists(path):
        return False
    text = open(path, 'r').read()
    if any([word in text for word in ["85.6", "25.0", "$"]]):
        return False
    return True


def grade_final_checkpoint():
    path = "/workspace/reimburse.txt"
    if not os.path.exists(path):
        return False
    text = open(path, 'r').read()
    if all([phrase.lower() in text.lower() for phrase in [
        "not qualified", "Credit card statements not accepted as receipts"
    ]]):
        return True
    return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = grade_final_checkpoint()
    checkpoints.append(Checkpoint(1, int(passed3)))

    return result
