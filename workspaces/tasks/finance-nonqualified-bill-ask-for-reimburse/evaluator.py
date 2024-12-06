import requests
import os

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import grader



@grader
def grade_final_checkpoint():
    path = "/workspace/reimburse.txt"
    if not os.path.exists(path):
        return False
    text = open(path, 'r').read()
    
    if any([word in text for word in ["85.6", "25.0", "$"]]):
        return False
    
    return sum([phrase.lower() in text.lower() for phrase in [
        "not qualified", "Credit card statements not accepted as receipts"
    ]])


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed = grade_final_checkpoint()
    checkpoints.append(Checkpoint(2, int(passed)))

    return result
