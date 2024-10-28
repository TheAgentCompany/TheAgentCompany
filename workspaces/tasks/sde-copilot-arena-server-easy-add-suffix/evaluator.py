import requests
import logging
import sys
import os
import json
from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final


def grade_checkpoint1():
    return os.path.exists("/workspace/copilot-arena-server")


def grade_checkpoint2():
    try:
        response = requests.get("http://localhost:5000/list_models")
        return response.status_code == 200
    except Exception:
        logging.warning("Local server is not launched correctly")
        return False


def grade_final_checkpoint():
    try:
        json_input = {
            "prefix": "test_prefix",
            "userId": "test_user",
            "privacy": "Private",
            "modelTags": [],
        }
        response = requests.post("http://localhost:5000/create_pair", json=json_input)
        return response.status_code == 400  # This should now fail
    except Exception:
        logging.warning("Local server is not launched correctly")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(2, int(grade_final_checkpoint())))
    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))
