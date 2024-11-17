import sys
import requests
import logging

from typing import List

from scoring import Result, Checkpoint
from common import *

# Configuration for gitlab
project_path = "root/openhands"


def get_gitlab_pipeline():
    try:
        response = make_gitlab_request(project_path, "pipelines")
        return response.json()
    except Exception as e:
        logging.error(f"Error occurred while checking the repository: {e}")
        return {}


@grader
def grade_checkpoint1(trajectory):
    return 'root/openhands/-/ci/editor' in trajectory


@grader
def grade_checkpoint2():
    msgs = get_gitlab_pipeline()
    return bool(msgs)


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    checkpoints.append(Checkpoint(2, 2 * int(grade_checkpoint2())))

    return result



