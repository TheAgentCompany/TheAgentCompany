import requests
import logging
import json
from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client
from config import *

# Create RocketChat instance
rocket = create_rocketchat_client()


############################# Helper Functions #####################################

# RocketChat checks
def check_channel_exists(channel_name):
    """Check if the specified channel exists in Rocket.Chat."""
    channels = rocket.channels_list().json().get("channels", [])
    return any(channel['name'] == channel_name for channel in channels)

def get_channel_room_id(channel_name):
    """Get the room_id for a specific channel."""
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

def check_url_1():
    """Check that the channel can be accessed at its URL."""
    url = f"{ROCKETCHAT_URL}/channel/sprint-planning"
    try:
        return check_channel_exists('sprint-planning') and requests.get(url).status_code == 200
    except requests.RequestException as e:
        print(f"Error checking URL: {e}")
        return False

# Plane checks
def get_project_id(project_name):
    """Get the project_id for a specific project by its name."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        data = response.json()
        projects = data.get('results', [])
        
        for project in projects:
            if project.get('name') == project_name:
                return project.get('id')
        
        print(f"Project with name '{project_name}' not found.")
    except requests.RequestException as e:
        print(f"Error: {e}")
    return None

def check_url_2(project_id):
    """Check that the project can be accessed at its URL."""
    url = f"{PLANE_BASEURL}/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    try:
        return requests.get(url).status_code == 200
    except requests.RequestException as e:
        print(f"Error checking URL: {e}")
        return False

def check_issue_created(project_id, issue_name):
    """Check if an issue with a specific name exists in a project using the Plane API."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        data = response.json()
        issues = data.get("results", [])
        for issue in issues:
            if issue.get('name') == issue_name:
                print(f"Issue '{issue_name}' found.")
                return True
        print(f"Issue '{issue_name}' not found.")
    except requests.RequestException as e:
        print(f"Error fetching issues: {e}")
    return False

def check_issue_assigned(project_id, issue_text, assignee):
    """Check if the issue is assigned to the correct participant."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        issues = response.json().get("results", [])
        for issue in issues:
            if issue.get('name') == issue_text:
                assignees = issue.get('assignees', [])
                # The assignees field contains user IDs, not usernames
                # We need to compare the assignee parameter with these IDs
                if assignee in assignees:
                    print(f"Issue '{issue_text}' is assigned to '{assignee}'.")
                    return True
                else:
                    print(f"Issue '{issue_text}' is not assigned to '{assignee}'. Assigned to: {assignees}")
                    return False
        print(f"Issue '{issue_text}' not found.")
    except requests.RequestException as e:
        print(f"Error fetching issues: {e}")
    return False

############################# Evaluator #####################################

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    # Checkpoint 1: Successfully accessed the sprint-planning channel in Rocket.Chat
    checkpoints.append(Checkpoint(1, int(check_url_1())))
    
    # Checkpoint 2: Created the project in Plane
    project_id = get_project_id("Frontend and Backend Enhancements")
    logging.info(f"Retrieved project_id: {project_id}")
    checkpoint2_pass = bool(project_id and check_url_2(project_id))
    checkpoints.append(Checkpoint(1, int(checkpoint2_pass)))
    
    # Checkpoint 3: Created issues with appropriate titles
    issues = [
        ('Implement new navigation bar', 'kritanjali.jain'),
        ('Set up backend API', 'john.doe'),
        ('Write unit tests for authentication', 'rocket.cat')
    ]
    all_issues_created = True
    for issue_text, assignee in issues:
        if not check_issue_created(project_id, issue_text):
            logging.warning(f"Checkpoint3 failed: Issue '{issue_text}' not created.")
            all_issues_created = False
        else:
            logging.info(f"Checkpoint3 passed: Issue '{issue_text}' created.")

    checkpoints.append(Checkpoint(1, int(all_issues_created))) 
    
    # Final Checkpoint: Assigned tasks to the correct individuals
    issues_and_assignees = [
        ('Implement new navigation bar', '84fc8acf-5167-47c1-afc3-b1c484cd49f7'),
        ('Set up backend API', '427323d8-8a42-4445-8c72-93d997f27f35'),
        ('Write unit tests for authentication', '4b52537b-5bec-49b3-b3ed-41fa601f4287')
    ]
    all_issues_assigned = True
    for issue_text, assignee in issues_and_assignees:
        if not check_issue_assigned(project_id, issue_text, assignee):
            logging.warning(f"Final checkpoint failed: Issue '{issue_text}' not assigned to '{assignee}'.")
            all_issues_assigned = False
        else:
            logging.info(f"Final checkpoint passed: Issue '{issue_text}' assigned to '{assignee}'.")

    checkpoints.append(Checkpoint(2, 2 * int(all_issues_assigned)))

    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))
