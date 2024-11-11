import requests
import logging
import os
import sys

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import checkpoint


@checkpoint
def grade_checkpoint1():
    return os.path.exists("/workspace/copilot-arena-server")


@checkpoint
def grade_checkpoint2(trajectory):
    return "requirements.txt" in trajectory


def grade_final_checkpoint():
    try:
        response = requests.get("http://localhost:5000/list_models")
        return response.status_code == 200
    except Exception:
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(3, 3 * int(passed1)))

    passed2 = grade_checkpoint2(trajectory)
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = grade_final_checkpoint()
    checkpoints.append(Checkpoint(3, 3 * int(passed3)))

    return result



