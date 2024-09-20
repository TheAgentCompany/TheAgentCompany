import os
import requests
from rocketchat_API.rocketchat import RocketChat

############################# Init Variables #####################################
# Rocket.Chat variables
ROCKETCHAT_HOSTNAME = os.getenv('ROCKETCHAT_HOSTNAME') or 'ogma.lti.cs.cmu.edu'


ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'


ROCKETCHAT_URL = f"http://{ROCKETCHAT_HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASS = 'jobbench'

# Plane variables
PLANE_HOSTNAME = os.getenv('PLANE_HOSTNAME') or 'ogma.lti.cs.cmu.edu'

PLANE_PORT = os.getenv('PLANE_PORT') or '8091'

PLANE_BASEURL = f"http://{PLANE_HOSTNAME}:{PLANE_PORT}"
PLANE_WORKSPACE_SLUG = os.getenv("PLANE_WORKSPACE_SLUG") or "cmu"
API_KEY = os.getenv('PLANE_API') 


headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

# Initialize RocketChat client
rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASS, server_url=ROCKETCHAT_URL)

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
    return check_channel_exists('sprint-planning') and requests.get(url).status_code == 200

# Plane checks
def get_project_id(project_identifier):
    """Get the project_id for a specific project by its identifier."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        projects = response.json().get("results", [])
        for project in projects:
            if project.get('identifier') == project_identifier:
                return project.get('id')
    return None

def check_url_2(project_id):
    """Check that the project can be accessed at its URL."""
    url = f"{PLANE_BASEURL}/{PLANE_WORKSPACE_SLUG}/projects/{project_id}"
    return requests.get(url).status_code == 200

def check_members(project_id, members):
    """Check if all participants are added as project members."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/members"
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        project_members = response.json().get("results", [])
        project_member_names = [member['user']['username'] for member in project_members]
        return all(member in project_member_names for member in members)
    return False

def check_issue_created(project_id, issue_text):
    """Check if an issue with a specific name exists in a project."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        issues = response.json().get("results", [])
        for issue in issues:
            if issue.get('name') == issue_text:
                return True
    return False

def check_issue_assigned(project_id, issue_text, assignee):
    """Check if the issue is assigned to the correct participant."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        issues = response.json().get("results", [])
        for issue in issues:
            if issue.get('name') == issue_text:
                assigned_users = [assignee_info['user']['username'] for assignee_info in issue.get('assignees', [])]
                return assignee in assigned_users
    return False

############################# Evaluator #####################################

def evaluate_task():
    points = 0

    # Checkpoint 1: Successfully accessed the sprint-planning channel in Rocket.Chat
    if check_url_1():
        print("Checkpoint 1 passed: Channel 'sprint-planning' exists and is accessible.")
        points += 1
    else:
        print("Checkpoint 1 failed: Channel 'sprint-planning' is not accessible.")
    
    # Checkpoint 2: Created the project in Plane
    project_id = get_project_id("Sprint-Frontend-Backend-Enhancements")
    if project_id and check_url_2(project_id):
        print("Checkpoint 2 passed: Project 'Sprint - Frontend and Backend Enhancements' created.")
        points += 1
    else:
        print("Checkpoint 2 failed: Project 'Sprint - Frontend and Backend Enhancements' not found or not accessible.")
    
    # Checkpoint 3: Added all participants as project members
    members = ['kritanjali.jain', 'John.Doe', 'rocket.cat']
    if project_id and check_members(project_id, members):
        print("Checkpoint 3 passed: All participants are added as project members.")
        points += 1
    else:
        print("Checkpoint 3 failed: Some participants are missing from the project.")
    
    # Final Checkpoint part 1 : Created issues with appropriate titles
    issues = [
        ('Implement new navigation bar', 'kritanjali.jain'),
        ('Set up backend API', 'john.doe'),
        ('Write unit tests for authentication', 'rocket.cat')
    ]
    all_issues_created = True
    for issue_text, assignee in issues:
        if not check_issue_created(project_id, issue_text):
            print(f"Final Checkpoint part 1 failed: Issue '{issue_text}' not created.")
            all_issues_created = False
        else:
            print(f"Final Checkpoint part 1 passed: Issue '{issue_text}' created.")
    
    if all_issues_created:
        points += 1
    
    # Final Checkpoint part 2 : Assigned tasks to the correct individuals
    all_issues_assigned = True
    for issue_text, assignee in issues:
        if not check_issue_assigned(project_id, issue_text, assignee):
            print(f"Final checkpoint part 2 failed: Issue '{issue_text}' not assigned to '{assignee}'.")
            all_issues_assigned = False
        else:
            print(f"Final checkpoint part 2 passed: Issue '{issue_text}' assigned to '{assignee}'.")

    if all_issues_assigned:
        points += 1

    # Final result
    print(f"Evaluation completed. Final score: {points}/5")
    return points

if __name__ == "__main__":
    evaluate_task()
