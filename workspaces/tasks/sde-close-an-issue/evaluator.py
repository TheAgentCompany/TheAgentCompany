import requests

import logging
from typing import List

from scoring import Result, Checkpoint
from common import *

project_path = "root/openhands" 
issue_iid = "3797"
target_comment = "Closing due to inactivity"


def grade_checkpoint1():
    try:
        comments_response = make_gitlab_request(project_path, f"issues/{issue_iid}/notes")
        comments_response.raise_for_status()
        comments_data = comments_response.json()
        has_target_comment = any(target_comment in comment['body'] for comment in comments_data)
        
        return has_target_comment
    except Exception as e:
        logging.error(f"Get comment failed: {e}")
        return False


def grade_checkpoint2():
    try: 
        issue_response = make_gitlab_request(project_path, f"issues/{issue_iid}")
        issue_response.raise_for_status()
        issue_data = issue_response.json()
        return issue_data['state'] == 'closed'
    except Exception as e:
        logging.error(f"Error fetching issue status: {e}")
    return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    return result



