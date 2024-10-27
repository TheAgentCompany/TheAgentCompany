import requests
from rocketchat_API.rocketchat import RocketChat
from config import *
from common import create_rocketchat_client

############################# Init Variables #####################################
CHANNEL_NAME = "sprint-planning"

# Create RocketChat instance
rocket = create_rocketchat_client()

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

def check_user_added(channel_name, username):
    """Check if a user is a member of a specific channel."""
    room_id = get_channel_room_id(channel_name)
    if not room_id:
        print(f"Failed to find room ID for channel #{channel_name}.")
        return False
    members_response = rocket.channels_members(channel=channel_name).json()
    members = members_response.get("members", [])
    return any(member['username'] == username for member in members)

def get_project_id(project_name):
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
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
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        issues = response.json().get('results', [])
        return any(issue['name'] == issue_name for issue in issues)
    except requests.RequestException as e:
        print(f"Error checking if issue exists: {e}")
    return False

############################# Pre-Initialization Tests #####################################

def pre_init_checks():
    # Check if the 'sprint-planning' channel exists
    if not check_channel_exists(CHANNEL_NAME):
        print(f"Channel '{CHANNEL_NAME}' does not exist.")
        return False
    else:
        print(f"Channel '{CHANNEL_NAME}' exists.")

    # Check if kritanjali.jain is added to the channel
    if not check_user_added(CHANNEL_NAME, 'kritanjali.jain'):
        print("User 'kritanjali.jain' is not added to the channel.")
        return False
    else:
        print("User 'kritanjali.jain' is added to the channel.")

    # Check if john.doe is added to the channel
    if not check_user_added(CHANNEL_NAME, 'John.Doe'):
        print("User 'john.doe' is not added to the channel.")
        return False
    else:
        print("User 'john.doe' is added to the channel.")

    # Check if rocket.cat is added to the channel
    if not check_user_added(CHANNEL_NAME, 'rocket.cat'):
        print("User 'rocket.cat' is not added to the channel.")
        return False
    else:
        print("User 'rocket.cat' is added to the channel.")

    # Check Plane project and issues
    project_name = "Frontend and Backend Enhancements"
    project_id = get_project_id(project_name)
    if not project_id:
        print(f"Project '{project_name}' not found in Plane.")
        return False
    else:
        print(f"Project '{project_name}' found in Plane.")

    # Check for 'Setup Backend API' issue
    if not check_issue_exists(project_id, 'Setup Backend API'):
        print("Issue 'Setup Backend API' not found in the project.")
        return False
    else:
        print("Issue 'Setup Backend API' found in the project.")

    # Check for 'Write unit tests for authentication' issue
    if not check_issue_exists(project_id, 'Write unit tests for authentication'):
        print("Issue 'Write unit tests for authentication' not found in the project.")
        return False
    else:
        print("Issue 'Write unit tests for authentication' found in the project.")

    return True

if __name__ == "__main__":
    if pre_init_checks():
        print("Pre-initialization checks passed.")
    else:
        print("Pre-initialization checks failed.")
