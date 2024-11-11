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


@checkpoint
def grade_checkpoint1(url='http://the-agent-company.com:8929/root/openhands/-/ci/editor?branch_name=main'):
    if len(sys.argv) < 2:
        trajectory = ""
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                trajectory = file.read()
        except Exception as e:
            print(f"Error reading trajectory file: {e}")
            exit(1)
    return url in trajectory


@checkpoint
def grade_checkpoint2():
    msgs = get_gitlab_pipeline()
    return bool(msgs)


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Define the scores corresponding to when each function is True
    scores = {
        grade_checkpoint1: 1,
        grade_checkpoint2: 2
    }

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func())))

    return result



