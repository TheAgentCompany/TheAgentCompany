import sys
import logging
import requests

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from config import *


PLANE_PROJECT_ID = "2bc631a1-8515-4bca-858e-129337c83c8d"

# Check if the title are in the trajectory
def grade_checkpoint1(trajectory):
    return ("[FEAT]: Unify evaluation prompt and episode rendering for human readers" in trajectory
            and "Roadmap to Sotopia v0.1" in trajectory)

# Check if the required issues exist on the project page
def grade_checkpoint2():
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{PLANE_PROJECT_ID}/issues/"
    
    try:
        response = requests.request("GET", url, headers=PLANE_HEADERS)

        if response.status_code == 200:
            resp = response.json()
            required_issues = [
                "[FEAT]: Unify evaluation prompt and episode rendering for human readers",
                "Roadmap to Sotopia v0.1"
            ]
            found_issues = set()
            for issue in resp.get("results", []):
                if issue.get('name') in required_issues:
                    found_issues.add(issue.get('name'))
            return len(found_issues) == len(required_issues)
        else:
            logging.warning(f"Invalid response: {response.json()}")
            return False
    except Exception as e:
        logging.warning(f"Error getting issues: {e}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))

    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
   
    return result



