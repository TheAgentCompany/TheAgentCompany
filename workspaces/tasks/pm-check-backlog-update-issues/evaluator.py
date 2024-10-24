import os
import requests
from common import create_rocketchat_client
from config import *
############################# Init Variables #####################################
# Create RocketChat instance
rocket = create_rocketchat_client()

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
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        projects = response.json().get('results', [])
        for project in projects:
            if project.get('name') == project_name:
                return project.get('id')
        print(f"Project with name '{project_name}' not found.")
    except requests.RequestException as e:
        print(f"Error: {e}")
    return None

def get_issue_details(project_id, issue_name):
    """Get details of a specific issue in a project."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        issues = response.json().get('results', [])
        for issue in issues:
            if issue.get('name') == issue_name:
                print(issue)
                return issue
        print(f"Issue with name '{issue_name}' not found.")
    except requests.RequestException as e:
        print(f"Error: {e}")
    return None

def check_message_posted(channel_name, content):
    """Check if a message containing specific content was posted in the specified channel."""
    room_id = get_channel_room_id(channel_name)
    if not room_id:
        return False
    messages = rocket.channels_history(room_id=room_id, count=10).json().get('messages', [])
    #print(messages)  # Keep this for debugging
    for message in messages:
        if message['u']['username'] == 'John.Doe':
            msg_content = message['msg'].lower()
            if any(keyword.lower() in msg_content for keyword in content):
                return True
    return False

def check_issue_comment(project_id, issue_id, mention):
    """Check if a comment mentioning a specific user exists on an issue."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/{issue_id}/comments/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        comments = response.json().get('results', [])
        return any(mention.lower() in comment['comment_html'].lower() for comment in comments)
    except requests.RequestException as e:
        print(f"Error checking issue comment: {e}")
    return False

def check_issue_state(issue, expected_groups):
    """
    Check if the issue's state belongs to any of the expected groups.
    
    :param issue: The issue object
    :param expected_groups: A list of expected state groups
    :return: True if the issue's state group is in expected_groups, False otherwise
    """
    workspace_slug = issue['workspace']
    project_id = issue['project']
    state_id = issue['state']
    
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{workspace_slug}/projects/{project_id}/states/{state_id}/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        state_details = response.json()
        state_group = state_details.get('group')
        return state_group in expected_groups
    except requests.HTTPError as e:
        if e.response.status_code == 403:
            print("Warning: Unable to access state details due to permissions. Making best guess based on available information.")
            # If we're checking for 'completed' and the issue has a 'completed_at' field, assume it's completed
            if 'completed' in expected_groups and issue.get('completed_at'):
                return True
            # If we're checking for 'backlog' or 'unstarted' and there's no 'completed_at', assume it's in one of these states
            elif set(['backlog', 'unstarted']) & set(expected_groups) and not issue.get('completed_at'):
                return True
        else:
            print(f"Error checking state group: {e}")
    except requests.RequestException as e:
        print(f"Error checking state group: {e}")
    return False

############################# Evaluator #####################################

def evaluate_task():
    points = 0
    project_name = "Frontend and Backend Enhancements"
    issue_name = "Set up backend API"
    
    # Checkpoint 1: Access the project
    project_id = get_project_id(project_name)
    if project_id:
        print("Checkpoint 1 passed: Project accessed on Plane.")
        points += 2
    else:
        print("Checkpoint 1 failed: Project not found on Plane.")
        return points

    # Checkpoint 2: Access the correct issue
    issue = get_issue_details(project_id, issue_name)
    if issue and issue['name'] == issue_name:
        print("Checkpoint 2 passed: Correct issue 'Set up backend API' accessed.")
        points += 2
    else:
        print("Checkpoint 2 failed: Correct issue 'Set up backend API' not found.")

    # Checkpoint 3, 4: Check for message in Rocket.Chat and for the correct response
    if check_message_posted('sprint-planning', ['update', 'completed', 'blocked']):
        print("Checkpoint 3 passed: Relevant message posted in #sprint-planning.")
        points += 2
    else:
        print("Checkpoint 3 failed: No relevant message found in #sprint-planning.")

    # Checkpoint 5: Check if issue status is updated to 'Done'
    if issue and check_issue_state(issue, ['completed']):
        print("Checkpoint 5 passed: Issue status updated to 'Done'.")
        points += 1
    else:
        print("Checkpoint 5 failed: Issue status not updated to 'Done'.")

    # Final checkpoint: Check for comment mentioning 'rocket.cat'
    if issue and check_issue_comment(project_id, issue['id'], 'rocket.cat'):
        print("Final checkpoint passed: Comment mentioning 'rocket.cat' found in the issue.")
        points += 1
    else:
        print("Final checkpoint failed: Comment mentioning 'rocket.cat' not found in the issue.")

    # Final result
    print(f"Evaluation completed. Final score: {points}/8")
    return points

if __name__ == "__main__":
    evaluate_task()
