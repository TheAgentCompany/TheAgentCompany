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
from common import checkpoint

@checkpoint
def grade_checkpoint1(trajectory):
    return "8929/root/api-server" in trajectory

@checkpoint
def grade_checkpoint2():
    if os.path.exists('/workspace/api-server/server.py'):
        with open('/workspace/api-server/server.py') as f:
            code_content = f.read()
            if "Welcome to the Flask API" in code_content:
                return True
    return False

def grade_final_checkpoint():
    try:
        response = requests.get("http://localhost:5432/welcome")
        return response.status_code == 200 and response.json() == {"message": "Welcome to the Flask API!"}
    except Exception:
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = grade_final_checkpoint()
    checkpoints.append(Checkpoint(2, 2 * int(passed3)))

    return result



