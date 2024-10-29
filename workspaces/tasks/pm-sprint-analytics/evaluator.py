import logging
import requests

from typing import List

from scoring import Result, Checkpoint
from config import *
from common import create_rocketchat_client

############################# Init Variables #####################################
# Create RocketChat instance
rocket = create_rocketchat_client()


############################# Helper Functions #####################################

def get_channel_room_id(channel_name):
    """Get the room_id for a specific channel."""
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

# Plane checks
def get_project_id(project_name):
    """Get the project_id for a specific project by its name."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
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

def get_cycle_details(project_id, cycle_name):
    """Get details of a specific cycle in a project."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/cycles/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        cycles = response.json().get('results', [])
        #print(cycles)
        for cycle in cycles:
            if cycle.get('name') == cycle_name:
                return cycle
        print(f"Cycle with name '{cycle_name}' not found.")
    except requests.RequestException as e:
        print(f"Error: {e}")
    return None

############################# Evaluator #####################################

def check_summary_posted(channel_name, required_keywords):
    """Check if a summary containing specific keywords was posted in the specified channel."""
    room_id = get_channel_room_id(channel_name)
    if not room_id:
        print(f"Channel '{channel_name}' not found.")
        return False
    
    messages = rocket.channels_history(room_id=room_id, count=20).json().get('messages', [])
    print(f"Checking last {len(messages)} messages in #{channel_name}")
    
    for message in messages:
        if message['u']['username'] == 'theagentcompany':  # Adjust this to the expected username
            msg_content = message['msg'].lower()
            if all(keyword.lower() in msg_content for keyword in required_keywords):
                print(f"Summary found in #{channel_name}")
                return True
    
    print(f"Summary not found in #{channel_name}")
    return False

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    project_name = "Frontend and Backend Enhancements"
    cycle_name = "Sprint 1"
    
    # Checkpoint 1: Access the project and cycle
    project_id = get_project_id(project_name)
    cycle = None
    if project_id:
        cycle = get_cycle_details(project_id, cycle_name)
        if cycle:
            logging.info("Checkpoint 1 passed: Project and Sprint 1 cycle accessed on Plane.")
            checkpoints.append(Checkpoint(1, 1))
        else:
            logging.warning("Checkpoint 1 failed: Sprint 1 cycle not found.")
            checkpoints.append(Checkpoint(1, 0))
    else:
        logging.warning("Checkpoint 1 failed: Project not found on Plane.")
        checkpoints.append(Checkpoint(1, 0))

    # Checkpoint 2: Collect and document metrics
    # Note: We can't directly verify the collected metrics, but we can check if they exist in the cycle details
    if cycle and cycle.get('total_issues') is not None and cycle.get('completed_issues') is not None:
        logging.info("Checkpoint 2 passed: Metrics collected.")
        checkpoints.append(Checkpoint(2, 2))
    else:
        logging.warning("Checkpoint 2 failed: Metrics not found in cycle details.")
        checkpoints.append(Checkpoint(2, 0))

    # Checkpoint 3: Post Sprint 1 Retrospective Summary
    required_keywords = ['sprint 1', 'retrospective', 'summary', 'completed issues', 'total issues']
    if check_summary_posted('sprint-planning', required_keywords):
        logging.info("Checkpoint 3 passed: Sprint 1 Retrospective Summary posted in #sprint-planning.")
        checkpoints.append(Checkpoint(2, 2))
    else:
        logging.warning("Checkpoint 3 failed: Sprint 1 Retrospective Summary not found in #sprint-planning.")
        checkpoints.append(Checkpoint(2, 0))

    return result



