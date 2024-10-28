import requests
import os
import logging
from datetime import datetime, timezone
from typing import List
import json

from scoring import Result, Checkpoint
from config import *

############################# init variable #####################################
HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
PLANE_PORT = os.getenv('PLANE_PORT') or '8091'
PLANE_BASEURL = f"http://{HOSTNAME}:{PLANE_PORT}"
PLANE_WORKSPACE_SLUG = os.getenv("PLANE_WORKSPACE_SLUG") or "tac"
PROJECT_NAME = "RisingWave"
PLANE_PROJECTS_URL = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"


headers = {
    "x-api-key": PLANE_API_KEY,
    "Content-Type": "application/json"
}

############################# helper functions #####################################

def get_project_id(project_name):
    """Get the project_id for a specific project by its name."""
    try:
        response = requests.get(PLANE_PROJECTS_URL, headers=headers)
        response.raise_for_status()
        projects = response.json().get('results', [])
        for project in projects:
            if project.get('name') == project_name:
                #print(project)
                return project.get('id')
        print(f"Project with name '{project_name}' not found.")
    except requests.RequestException as e:
        print(f"Error: {e}")
    return None

def get_active_and_upcoming_cycles(project_url):
    """Get the active and upcoming cycles for a project using timestamps."""
    url = f"{project_url}/cycles/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        cycles = response.json().get('results', [])
        now = datetime.now(timezone.utc)
        active_cycle = None
        upcoming_cycle = None
        for cycle in cycles:
            # Convert start_date and end_date to offset-aware UTC datetimes
            start_date = datetime.fromisoformat(cycle['start_date']).replace(tzinfo=timezone.utc)
            end_date = datetime.fromisoformat(cycle['end_date']).replace(tzinfo=timezone.utc)
            if start_date <= now <= end_date:
                active_cycle = cycle
            elif start_date > now:
                if not upcoming_cycle or start_date < datetime.fromisoformat(upcoming_cycle['start_date']).replace(tzinfo=timezone.utc):
                    upcoming_cycle = cycle
        return active_cycle, upcoming_cycle
    except requests.RequestException as e:
        print(f"Error: {e}")
    return None, None

def get_cycle_issues(project_url,cycle_id):
    """Get issues for a specific cycle."""
    url = f"{project_url}/cycles/{cycle_id}/cycle-issues/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.RequestException as e:
        print(f"Error: {e}")
    return []

def get_issues(project_url):
    """Get issues for a specific cycle."""
    url = f"{project_url}/issues/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.RequestException as e:
        print(f"Error: {e}")
    return []

def get_state_details(project_url,state_id):
    """Get state details for a specific state."""
    url = f"{project_url}/states/{state_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error: {e}")
    return None

def get_issue_by_name(issues, name):
    target_issues = [issue for issue in issues if issue['name'] == name]
    if len(target_issues) == 0:
        logging.info(f"Issue '{name}' not found in the cycle")
        return None
    return target_issues[0]

############################# grade checkpoints #####################################

def grade_checkpoint1(project_url, active_cycle_issues):
    target_issue = get_issue_by_name(active_cycle_issues, 'Evaluate data throughput')
    if target_issue is None:
        return False
    state_details = get_state_details(project_url, target_issue['state'])
    if not state_details:
        logging.error("Error getting state details")
        return False
    if state_details['name'] == 'Done':
        return True
    logging.info(f"State of issue 'Evaluate data throughput' is {state_details['name']}, expected 'Done'")
    return False

def grade_checkpoint2(project_url, all_issues):
    target_issue = get_issue_by_name(all_issues, 'Decrease database latency')
    if target_issue is None:
        return False
    state_details = get_state_details(project_url,target_issue['state'])
    if not state_details:
        logging.error("Error getting state details")
        return False
    if state_details['name'] == 'In Progress':
        return True
    logging.info(f"State of issue 'Decrease database latency' is {state_details['name']}, expected 'In Progress'")
    return False

def grade_checkpoint3(next_cycle_issues):
    target_issue = get_issue_by_name(next_cycle_issues, 'Decrease database latency')
    if target_issue is None:
        logging.info("Issue 'Decrease database latency' not moved to the next cycle")
        return False
    return True


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    project_id = get_project_id(PROJECT_NAME)
    project_url = f"{PLANE_PROJECTS_URL}{project_id}/"
    active_cycle, upcoming_cycle = get_active_and_upcoming_cycles(project_url)
    active_cycle_issue_ids = [issue['id'] for issue in get_cycle_issues(project_url,active_cycle['id'])]
    next_cycle_issues_ids = [issue['id'] for issue in get_cycle_issues(project_url,upcoming_cycle['id'])]
    all_issues = get_issues(project_url)
    active_cycle_issues = [issue for issue in all_issues if issue['id'] in active_cycle_issue_ids]
    next_cycle_issues = [issue for issue in all_issues if issue['id'] in next_cycle_issues_ids]

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(project_url, active_cycle_issues))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2(project_url, all_issues))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3(next_cycle_issues))))

    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))
