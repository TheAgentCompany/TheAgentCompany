import logging
import sys
import urllib.parse

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import *

project_path = "root/opensearch"
stale_branch = "feature/ssl"

def check_repository_exists():
    try:
        response = make_gitlab_request(project_path)
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Error occurred while checking the repository: {e}")
        return False

def check_branch_deleted():
    encoded_branch = urllib.parse.quote(stale_branch, safe='')
    try:
        response = make_gitlab_request(project_path, f"repository/branches/{encoded_branch}")
        return response.status_code == 404
    except Exception as e:
        logging.error(f"Error occurred while checking the branch: {e}")
        return False

def grade_checkpoint1(trajectory):
    target_context = "permanently delete the branch"
    
    try:
        return target_context in trajectory
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint1: {e}")
        return False

def grade_checkpoint2():
    repo_exists = check_repository_exists()
    branch_deleted = check_branch_deleted()
    
    if repo_exists and branch_deleted:
        logging.info("Repository exists and branch 'feature/ssl' is deleted.")
        return True
    else:
        logging.warning(f"Repository exists: {repo_exists}, Branch deleted: {branch_deleted}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    checkpoints.append(Checkpoint(1, grade_checkpoint1(trajectory)))
    checkpoints.append(Checkpoint(1, grade_checkpoint2()))

    return result



