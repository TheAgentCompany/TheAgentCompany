import os
import requests

############################# init variable ##################################### 
HOSTNAME = os.getenv('PLANE_HOSTNAME') or 'ogma.lti.cs.cmu.edu'
PLANE_PORT = os.getenv('PLANE_PORT') or '8091'
PLANE_BASEURL = f"http://{HOSTNAME}:{PLANE_PORT}"
PLANE_WORKSPACE_SLUG = os.getenv("PLANE_WORKSPACE_SLUG") or "cmu"
API_KEY = os.getenv('PLANE_API')
headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
}

def check_url_1(project_id, browser_logs):
    return f"{PLANE_BASEURL}/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues" in browser_logs


def get_project_id(project_identifier):
    """Get the project_id for a specific project by its human identifier."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        resp = response.json()
        for project in resp["results"]:
            if project.get('identifier') == project_identifier:
                return project.get('id')
    return None

def check_issue(project_id, issue_text):
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        resp = response.json()
        for issue in resp["results"]:
            if issue.get('name') == issue_text:
                return True
    return False

if __name__ == "__main__":
    project_id = get_project_id("WEBARENA")
    print(check_url_1(project_id, f"ACTION: goto('{PLANE_BASEURL}/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues"))
    print(check_issue(project_id, "Fix page loading performance"))
