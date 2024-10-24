import os
import requests
from rocketchat_API.rocketchat import RocketChat
from config import *
############################# Init Variables #####################################
# Rocket.Chat variables
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com' 
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'

ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"

# Plane variables
PLANE_HOSTNAME = os.getenv('PLANE_HOSTNAME') or 'the-agent-company.com'
    
PLANE_PORT =  os.getenv('PLANE_PORT') or '8091'


PLANE_BASEURL = f"http://{PLANE_HOSTNAME}:{PLANE_PORT}"
PLANE_WORKSPACE_SLUG = os.getenv("PLANE_WORKSPACE_SLUG") or "cmu" 

headers = {
    "x-api-key": PLANE_API_KEY,
    "Content-Type": "application/json"
}

from common import create_rocketchat_client

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

# Plane checks
def get_project_id(project_name):
    """Get the project_id for a specific project by its name."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    try:
        response = requests.get(url, headers=headers)
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
        response = requests.get(url, headers=headers)
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

def evaluate_task():
    points = 0
    project_name = "Frontend and Backend Enhancements"
    cycle_name = "Sprint 1"
    
    # Checkpoint 1: Access the project and cycle
    project_id = get_project_id(project_name)
    if project_id:
        cycle = get_cycle_details(project_id, cycle_name)
        if cycle:
            print("Checkpoint 1 passed: Project and Sprint 1 cycle accessed on Plane.")
            points += 1
        else:
            print("Checkpoint 1 failed: Sprint 1 cycle not found.")
            return points
    else:
        print("Checkpoint 1 failed: Project not found on Plane.")
        return points

    # Checkpoint 2: Collect and document metrics
    # Note: We can't directly verify the collected metrics, but we can check if they exist in the cycle details
    if cycle.get('total_issues') is not None and cycle.get('completed_issues') is not None:
        print("Checkpoint 2 passed: Metrics collected.")
        points += 2
    else:
        print("Checkpoint 2 failed: Metrics not found in cycle details.")

    # Checkpoint 3: Post Sprint 1 Retrospective Summary
    required_keywords = ['sprint 1', 'retrospective', 'summary', 'completed issues', 'total issues']
    if check_summary_posted('sprint-planning', required_keywords):
        print("Checkpoint 3 passed: Sprint 1 Retrospective Summary posted in #sprint-planning.")
        points += 2
    else:
        print("Checkpoint 3 failed: Sprint 1 Retrospective Summary not found in #sprint-planning.")

    # Final result
    print(f"Evaluation completed. Final score: {points}/5")
    return points

if __name__ == "__main__":
    evaluate_task()
