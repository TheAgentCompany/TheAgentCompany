import requests
import sys

from common import create_rocketchat_client, get_chat_history
rocket=create_rocketchat_client()

PLANE_BASEURL = "http://the-agent-company.com:8091"
PLANE_WORKSPACE_SLUG = "tac"
api_key = "plane_api_f41b459d30bb4e389ec0b9142bfac8cd"
headers = {"x-api-key": api_key,"Content-Type": "application/json"}

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

def checkpoint1():
    if len(sys.argv) < 2:
        trajectory = ""
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                trajectory = file.read()
        except Exception as e:
            print(f"Error reading trajectory file: {e}")
            return False
    return "http://the-agent-company.com:8091/tac/projects/73cb74f7-a7ac-4292-a915-e2f59a09a703/issues/8eba9853-4178-42a6-b113-e66002e8e0ab" in trajectory and "http://the-agent-company.com:8091/tac/projects/73cb74f7-a7ac-4292-a915-e2f59a09a703/issues/5d1c8695-acfd-44c2-8d2d-e41c67cdd8c0" in trajectory

def checkpoint2():
    if len(sys.argv) < 2:
        trajectory = ""
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                trajectory = file.read()
        except Exception as e:
            print(f"Error reading trajectory file: {e}")
            return False
    return "http://the-agent-company.com:3000/home" in trajectory

def checkpoint3():
    msgs_1 = get_chat_history(rocket, username='mike_chen')
    msgs_2 = get_chat_history(rocket, username='wang_fang')
    return bool(msgs_1) and bool(msgs_2)

def checkpoint4():
    project_name = "OpenHands"
    issue_name_1 = "Model: recall rate is 0"
    issue_name_2 = "Model: security problem"

    project_id = get_project_id(project_name)

    issue_1 = get_issue_details(project_id, issue_name_1)
    issue_2 = get_issue_details(project_id, issue_name_2)


    state_1 = issue_1.get('state') == '1d28d389-3228-4e28-90f6-6dd7adb6ccb3'
    state_2 = issue_2.get('state') == '1be22ae7-46fd-456f-8ca2-c32fd4f8040a'

    return bool(state_1) and bool(state_2)


def calculate_total_score():
    # Define the scores corresponding to when each function is True
    scores = {
        checkpoint1: 1,
        checkpoint2: 1,
        checkpoint3: 2,
        checkpoint4: 2,

    }

    total_score = 0

    for func, score in scores.items():
        if func():
            total_score += score

    return total_score

# compute the total point
total = calculate_total_score()
print(f"\ntotal point is: {total}")


