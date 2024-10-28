import requests
import json
import logging
from common import create_rocketchat_client
from config import *


############################# Initialization Variables #####################################
CHANNEL_NAME = "sprint-planning"
# Create RocketChat instance
rocket = create_rocketchat_client()

############################# Logging Setup #####################################  
logging.basicConfig(level=logging.INFO,    
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()  # Log messages to the console
    ])
logger = logging.getLogger("Data Population")


def get_project_id(project_name):
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        projects = response.json().get('results', [])
        for project in projects:
            if project.get('name') == project_name:
                return project.get('id')
        logger.error(f"Project with name '{project_name}' not found.")
    except requests.RequestException as e:
        logger.error(f"Error getting project ID: {e}")
    return None

def create_issue(project_id, name, state_group):
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    data = {
        "name": name,
        "state_group": state_group
    }
    try:
        response = requests.post(url, headers=PLANE_HEADERS, data=json.dumps(data))
        response.raise_for_status()
        logger.info(f"Successfully created issue '{name}' with state group '{state_group}'")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to create issue '{name}': {e}")
    return None

def issue_exists(project_id, name):
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        issues = response.json().get('results', [])
        return any(issue['name'] == name for issue in issues)
    except requests.RequestException as e:
        logger.error(f"Error checking if issue exists: {e}")
    return False

############################# Utility Functions ##################################### 

def create_channel(channel_name):
    response = rocket.channels_create(channel_name).json()
    if response.get('success'):
        logger.info(f"Successfully created channel {channel_name}.")
        return response['channel']['_id']
    else:
        logger.error(f"Failed to create channel {channel_name}: {response.get('error')}")
        return None

def post_message(user_credentials, channel_id, message):
    user_rocket = create_rocketchat_client(user_credentials['username'], user_credentials['password'])
    response = user_rocket.chat_post_message(message, room_id=channel_id).json()
    if response.get('success'):
        logger.info(f"Message posted to channel by {user_credentials['username']}.")
    else:
        logger.error(f"Failed to post message by {user_credentials['username']}: {response.get('error')}")

def add_user_to_channel(channel_id, username):
    """Add a user to the specified channel using the user ID."""
    # Get user info to fetch the user_id
    user_info = rocket.users_info(username=username).json()
    
    if user_info.get('success'):
        user_id = user_info['user']['_id']
        # Invite user to the channel using user_id
        response = rocket.channels_invite(room_id=channel_id, user_id=user_id).json()
        
        if response.get('success'):
            logger.info(f"Successfully added {username} to the channel.")
        else:
            logger.error(f"Failed to add {username} to the channel: {response.get('error')}")
    else:
        logger.error(f"Failed to get info for user {username}: {user_info.get('error')}")

def user_exists(username):
    """Check if a user exists in RocketChat."""
    response = rocket.users_info(username=username).json()
    if response.get('success'):
        logger.info(f"User {username} already exists.")
        return True
    else:
        logger.info(f"User {username} does not exist.")
        return False


def setup_user(user_name, password, email, username):
    # Check if user already exists
    if user_exists(username):
        return {'username': username, 'password': password}
    response = rocket.users_create(email, user_name, password, username).json()
    if response.get('success'):
        logger.info(f"Successfully created user {username}.")
        return {'username': username, 'password': password}
    else:
        logger.error(f"Failed to create user {username}: {response.get('error')}")
        return None

############################# Population Script ##################################### 


def populate_channel():
    # Create the sprint-planning channel
    channel_id = create_channel(CHANNEL_NAME)
    if not channel_id:
        return

    # Define user credentials
    users = [
        {'name': 'John Doe', 'password': 'John.Doe', 'email': 'John.Doe@cmu.edu.com', 'username': 'John.Doe'},
        {'name': 'Rocket Cat', 'password': 'theagentcompany', 'email': 'rocket.Cat@email.com', 'username': 'rocket.cat'}
    ]

    user_credentials_list = []

    # First, set up users and add them to the channel
    for user in users:
        user_credentials = setup_user(user['name'], user['password'], user['email'], user['username'])
        if user_credentials:
            user_credentials_list.append(user_credentials)
            # Add user to the 'sprint-planning' channel
            add_user_to_channel(channel_id, user['username'])

    # Populate Plane with issues
    project_name = "Frontend and Backend Enhancements"
    project_id = get_project_id(project_name)
    
    if project_id:
        # Create 'Setup Backend API' issue if it doesn't exist
        if not issue_exists(project_id, 'Setup Backend API'):
            create_issue(project_id, 'Setup Backend API', 'started')
        else:
            logger.info("Issue 'Setup Backend API' already exists")

        # Create 'Write unit tests for authentication' issue
        if not issue_exists(project_id, 'Write unit tests for authentication'):
            create_issue(project_id, 'Write unit tests for authentication', 'backlog')
        else:
            logger.info("Issue 'Write unit tests for authentication' already exists")
    else:
        logger.error(f"Failed to find project '{project_name}'")

if __name__ == "__main__":
    populate_channel()
