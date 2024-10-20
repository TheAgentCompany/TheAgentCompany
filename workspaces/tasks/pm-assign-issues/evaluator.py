import os
import requests
from common import create_rocketchat_client

############################# Init Variables #####################################
# Create RocketChat instance
rocket = create_rocketchat_client()

SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"

# Plane variables
PLANE_HOSTNAME = os.getenv('PLANE_HOSTNAME') or 'the-agent-company.com'

PLANE_PORT =  os.getenv('PLANE_PORT') or '8091'

PLANE_BASEURL = f"http://{PLANE_HOSTNAME}:{PLANE_PORT}"
PLANE_WORKSPACE_SLUG = os.getenv("PLANE_WORKSPACE_SLUG") or "cmu"

API_KEY = os.getenv('PLANE_API') 


headers = {
    "x-api-key": API_KEY,
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
        response = requests.get(url, headers=headers)
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
        response = requests.get(url, headers=headers)
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

def evaluate_task():
    points = 0

    # Checkpoint 1: Successfully accessed the sprint-planning channel in Rocket.Chat
    if check_url_1():
        print("Checkpoint 1 passed: Channel 'sprint-planning' exists and is accessible.")
        points += 1
    else:
        print("Checkpoint 1 failed: Channel 'sprint-planning' is not accessible.")
    
    # Checkpoint 2: Created the project in Plane
    project_id = get_project_id("Frontend and Backend Enhancements")
    print(f"Retrieved project_id: {project_id}")  # Debug print
    if project_id and check_url_2(project_id):
        print("Checkpoint 2 passed: Project 'Frontend and Backend Enhancements' created.")
        points += 1
    else:
        print("Checkpoint 2 failed: Project 'Frontend and Backend Enhancements' not found or not accessible.")
    
    # Checkpoint 3: Added all participants as project members
    # Passes if Final Checkpoint part 2 passes

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
    issues_and_assignees = [
        ('Implement new navigation bar', '84fc8acf-5167-47c1-afc3-b1c484cd49f7'),
        ('Set up backend API', '427323d8-8a42-4445-8c72-93d997f27f35'),
        ('Write unit tests for authentication', '4b52537b-5bec-49b3-b3ed-41fa601f4287')
    ]
    all_issues_assigned = True
    for issue_text, assignee in issues_and_assignees:
        if not check_issue_assigned(project_id, issue_text, assignee):
            print(f"Final checkpoint part 2 failed: Issue '{issue_text}' not assigned to '{assignee}'.")
            all_issues_assigned = False
        else:
            print(f"Final checkpoint part 2 passed: Issue '{issue_text}' assigned to '{assignee}'.")

    if all_issues_assigned:
        points += 2

    # Final result
    print(f"Evaluation completed. Final score: {points}/5")
    return points

if __name__ == "__main__":
    evaluate_task()
