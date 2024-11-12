import logging
import requests

from typing import List

from scoring import Result, Checkpoint
from common import *

project_path = "root/raft"

# Check if the repository returns a 404 status via the API.
@grader
def check_repository_deleted():
    
    try:
        response = make_gitlab_request(project_path)
 
        if response is not None and response.status_code == 404:
            logging.info(f"Repository '{project_path}' not found (404), as expected.")
            return True
        else:
            logging.error(f"Unexpected response: {response}")
            return False
    except requests.RequestException as e:
        logging.error(f"Error occurred while checking the repository: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    checkpoints.append(Checkpoint(1, check_repository_deleted()))
    return result



