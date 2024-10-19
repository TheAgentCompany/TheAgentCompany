import os
import requests
from rocketchat_API.rocketchat import RocketChat

############################# Init Variables #####################################
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
ROCKETCHAT_PORT =  os.getenv('ROCKETCHAT_PORT') or '3000'
CHANNEL_NAME = "sprint-planning"
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASS = 'jobbench'

# Initialize the RocketChat client with admin username and password
rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASS, server_url=ROCKETCHAT_URL)

# Add Plane API variables
PLANE_HOSTNAME = os.getenv('PLANE_HOSTNAME') or 'the-agent-company.com'
PLANE_PORT = os.getenv('PLANE_PORT') or '8091'
PLANE_BASEURL = f"http://{PLANE_HOSTNAME}:{PLANE_PORT}"
PLANE_WORKSPACE_SLUG = os.getenv("PLANE_WORKSPACE_SLUG") or "cmu"
API_KEY = os.getenv('PLANE_API') 

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

############################# Helper Functions #####################################

def check_channel_exists(channel_name):
    """Check if the specified channel exists."""
    response = rocket.channels_list().json()
    channels = response.get("channels", [])
    return any(channel['name'] == channel_name for channel in channels)

def get_channel_room_id(channel_name):
    """Get the room_id for a specific channel by its name."""
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

def get_project_id(project_name):
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        projects = response.json().get('results', [])
        for project in projects:
            if project.get('name') == project_name:
                return project.get('id')
    except requests.RequestException as e:
        print(f"Error getting project ID: {e}")
    return None

def check_issue_exists(project_id, issue_name):
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        issues = response.json().get('results', [])
        return any(issue['name'] == issue_name for issue in issues)
    except requests.RequestException as e:
        print(f"Error checking if issue exists: {e}")
    return False

def check_cycle_exists(project_id, cycle_name):
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/cycles/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        cycles = response.json().get('results', [])
        return any(cycle['name'] == cycle_name for cycle in cycles)
    except requests.RequestException as e:
        print(f"Error checking if cycle exists: {e}")
    return False

############################# Pre-Initialization Tests #####################################

def pre_init_checks():
    # Check if the 'sprint-planning' channel exists
    if not check_channel_exists(CHANNEL_NAME):
        print(f"Channel '{CHANNEL_NAME}' does not exist.")
        return False
    else:
        print(f"Channel '{CHANNEL_NAME}' exists.")

    # Check Plane project and issues
    project_name = "Frontend and Backend Enhancements"
    project_id = get_project_id(project_name)
    if not project_id:
        print(f"Project '{project_name}' not found in Plane.")
        return False
    else:
        print(f"Project '{project_name}' found in Plane.")

    # Check for 'Sprint 1' cycle
    if not check_cycle_exists(project_id, 'Sprint 1'):
        print("Cycle 'Sprint 1' not found in the project.")
        return False
    else:
        print("Cycle 'Sprint 1' found in the project.")

    # Check for 'Sprint 2' cycle
    if not check_cycle_exists(project_id, 'Sprint 2'):
        print("Cycle 'Sprint 2' not found in the project.")
        return False
    else:
        print("Cycle 'Sprint 2' found in the project.")

    return True



if __name__ == "__main__":
    if pre_init_checks():
        print("Pre-initialization checks passed.")
    else:
        print("Pre-initialization checks failed.")
