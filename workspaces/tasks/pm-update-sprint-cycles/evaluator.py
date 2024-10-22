import os
import requests
from rocketchat_API.rocketchat import RocketChat
from datetime import datetime, timezone

############################# Init Variables #####################################
# Rocket.Chat variables
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com' 
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'

ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASS = 'jobbench'

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

from common import create_rocketchat_client

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

def get_active_and_upcoming_cycles(project_id):
    """Get the active and upcoming cycles for a project using timestamps."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/cycles/"
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
            print(f"Cycle: {cycle['name']}, Start: {start_date}, End: {end_date}")
            if start_date <= now <= end_date:
                print(now)
                active_cycle = cycle
                print(f"Active cycle: {active_cycle}")
            elif start_date > now:
                if not upcoming_cycle or start_date < datetime.fromisoformat(upcoming_cycle['start_date']).replace(tzinfo=timezone.utc):
                    upcoming_cycle = cycle
                    print(f"Upcoming cycle: {upcoming_cycle}")
        return active_cycle, upcoming_cycle
    except requests.RequestException as e:
        print(f"Error: {e}")
    return None, None

def get_cycle_issues(project_id, cycle_id):
    """Get issues for a specific cycle."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.RequestException as e:
        print(f"Error: {e}")
    return []

############################# Evaluator #####################################
def check_issue_state(issue, expected_groups):
    """
    Check if the issue's state belongs to any of the expected groups.
    
    :param issue: The issue object
    :param expected_groups: A list of expected state groups
    :return: True if the issue's state group is in expected_groups, False otherwise
    """
    workspace_slug = issue['workspace']
    project_id = issue['project']
    issue_id = issue['id']
    
    # First, get the issue details to retrieve the state ID
    issue_url = f"{PLANE_BASEURL}/api/v1/workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/"
    try:
        issue_response = requests.get(issue_url, headers=headers)
        issue_response.raise_for_status()
        issue_details = issue_response.json()
        state_id = issue_details['state']
        
        # Now, get the state details
        state_url = f"{PLANE_BASEURL}/api/v1/workspaces/{workspace_slug}/projects/{project_id}/states/{state_id}/"
        state_response = requests.get(state_url, headers=headers)
        state_response.raise_for_status()
        state_details = state_response.json()
        state_group = state_details.get('group')
        
        return state_group in expected_groups
    except requests.RequestException as e:
        print(f"Error checking state group: {e}")
    return False

def check_issues_moved(active_cycle, upcoming_cycle, project_id, issue_names):
    """Check if specified issues are in the correct cycle."""
    if not active_cycle or not upcoming_cycle:
        return False

    active_cycle_id = active_cycle['id']
    upcoming_cycle_id = upcoming_cycle['id']

    active_issues = get_cycle_issues(project_id, active_cycle_id)
    print(active_issues)    
    upcoming_issues = get_cycle_issues(project_id, upcoming_cycle_id)
    print(upcoming_issues)

    results = []
    for issue_name in issue_names:
        active_issue = next((issue for issue in active_issues if issue['name'] == issue_name), None)
        upcoming_issue = next((issue for issue in upcoming_issues if issue['name'] == issue_name), None)
        
        
        if active_issue:
            print(active_issue)
            if check_issue_state(active_issue, ['backlog', 'unstarted', 'started']):
                results.append(False)  # Issue should have been moved but wasn't
            elif check_issue_state(active_issue, ['completed']):
                results.append(True)  # Completed issue correctly in active cycle
            else:
                results.append(False)  # Issue in unexpected state
        elif upcoming_issue:
            print(upcoming_issue)
            if check_issue_state(upcoming_issue, ['backlog', 'unstarted', 'started']):
                results.append(True)  # Issue correctly moved to upcoming cycle
            else:
                results.append(False)  # Issue in unexpected state in upcoming cycle
        else:
            results.append(False)  # Issue not found in either cycle

    return all(results)

def check_notifications_sent(channel_name):
    """Check if notifications were sent for moved issues."""
    room_id = get_channel_room_id(channel_name)
    if not room_id:
        print(f"Channel '{channel_name}' not found.")
        return False
    
    messages = rocket.channels_history(room_id=room_id, count=20).json().get('messages', [])
    for message in messages:
        if message['u']['username'] == 'jobbench':  # Adjust this to the expected username
            if 'has been moved to the next sprint' in message['msg']:
                return True
    return False

def evaluate_task():
    points = 0
    project_name = "Frontend and Backend Enhancements"
 
    
    # Checkpoint 1: Access the project and cycles
    project_id = get_project_id(project_name)
    if project_id:
        active_cycle, upcoming_cycle = get_active_and_upcoming_cycles(project_id)
        if active_cycle and upcoming_cycle:
            print("Checkpoint 1 passed: Project and cycles accessed on Plane.")
            points += 1
        else:
            print("Checkpoint 1 failed: Active or upcoming cycle not found.")
            return points
    else:
        print("Checkpoint 1 failed: Project not found on Plane.")
        return points

    # Checkpoint 2: Move unfinished issues
    issues_to_check = ["Set up backend API", "Implement new navigation bar", "Write unit tests for authentication"]  # Replace with actual issue names
    if check_issues_moved(active_cycle, upcoming_cycle, project_id, issues_to_check):
        print("Checkpoint 2 passed: Issues are in the correct cycles.")
        points += 2
    else:
        print("Checkpoint 2 failed: Some issues are not in the correct cycles.")

    # Checkpoint 3: Notify assignees
    if check_notifications_sent('sprint-planning'):
        print("Checkpoint 3 passed: Notifications sent in #sprint-planning.")
        points += 2
    else:
        print("Checkpoint 3 failed: Notifications not found in #sprint-planning.")

    # Final result
    print(f"Evaluation completed. Final score: {points}/5")
    return points

if __name__ == "__main__":
    evaluate_task()
