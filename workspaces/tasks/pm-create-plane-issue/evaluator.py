import requests
import logging
import json
from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from config import *


def get_project_id(project_identifier):
    """Get the project_id for a specific project by its human identifier."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    try:
        response = requests.request("GET", url, headers=PLANE_HEADERS)
    except requests.RequestException as e:
        logging.warning(f"Error getting project id: {e}")
        return None
    if response.status_code == 200:
        resp = response.json()
        for project in resp["results"]:
            if project.get('identifier') == project_identifier:
                return project.get('id')
    return None

def grade_checkpoint1(trajectory, project_id):
    return f"{PLANE_BASEURL}/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues" in trajectory


def grade_checkpoint2(project_id):
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    try:
        response = requests.request("GET", url, headers=PLANE_HEADERS)
    except requests.RequestException as e:
        logging.warning(f"Error getting issues: {e}")
        return False

    if response.status_code == 200:
        resp = response.json()
        for issue in resp.get("results", []):
            if issue.get('name').lower() == "Improve page loading speed".lower():
                return True
    return False


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    project_id = get_project_id("wdash")
    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory, project_id))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2(project_id))))
    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))