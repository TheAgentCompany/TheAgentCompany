import os
import requests
import sys
import logging
from const import *
############################# init variable ##################################### 
HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
PLANE_PORT = os.getenv('PLANE_PORT') or '8091'
PLANE_BASEURL = f"http://{HOSTNAME}:{PLANE_PORT}"
PLANE_WORKSPACE_SLUG = os.getenv("PLANE_WORKSPACE_SLUG") or "tac"
headers = {
    "x-api-key": PLANE_API_KEY,
    "Content-Type": "application/json"
}


def get_project_id(project_identifier):
    """Get the project_id for a specific project by its human identifier."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    try:
        response = requests.request("GET", url, headers=headers)
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
        response = requests.request("GET", url, headers=headers)
    except requests.RequestException as e:
        logging.warning(f"Error getting issues: {e}")
        return False

    if response.status_code == 200:
        resp = response.json()
        for issue in resp.get("results", []):
            if issue.get('name').lower() == "Improve page loading speed".lower():
                return True
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.warning("No trajectory file provided, partial credit might not be granted")
        trajectory = ""
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                trajectory = file.read()
        except Exception as e:
            print(f"Error reading trajectory file: {e}")
            exit(1)
    project_id = get_project_id("wdash")
    passed1 = grade_checkpoint1(trajectory, project_id)
    passed2 = grade_checkpoint2(project_id)
    points = 0
    if passed2:
        points = 2
    elif passed1:
        points = 1
    print(f"Final points for task: {points}")