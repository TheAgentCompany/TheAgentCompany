"""Summary of evaluator for example task

You don't have to write a summary for the evaluator, although documentation is
strongly encouraged.

A good evaluator should:
1. be robust - it shouldn't abort because of its own bug or lack of fail over mechanism
2. be deterministic and idempotent
3. grant partial credits if possible
4. encourage but not require trajectory for grading
"""

import requests
import os

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final


def grade_checkpoint1(trajectory):
    policy_file_path = "https://ogma.lti.cs.cmu.edu/apps/files/files/1363?dir=/Documents/Administrative%20Specialist"
    return policy_file_path in trajectory

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
