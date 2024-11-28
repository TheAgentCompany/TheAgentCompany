import requests
import os

SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'localhost'
PLANE_PORT = os.getenv('PLANE_PORT') or '8091'
PLANE_BASEURL = f"http://{SERVER_HOSTNAME}:{PLANE_PORT}"
PLANE_WORKSPACE_SLUG = os.getenv("PLANE_WORKSPACE_SLUG") or "tac"
PLANE_API_KEY = os.environ.get("PLANE_API_KEY") or "plane_api_83f868352c6f490aba59b869ffdae1cf"
PLANE_HEADERS = {
    "x-api-key": PLANE_API_KEY,
    "Content-Type": "application/json"
}

def login_to_plane():
    res = []
    try:
        res = get_all_plane_projects()
        if len(res) == 0:
            return 400, "failed to login"
        else:
            return 200, "login success"
    except Exception as e:
        print(f"{e}")
        return 400, "failed to login"

def get_all_plane_projects():
    """Get all projects in plane."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        return response.json().get('results', [])
    except Exception as e:
        print(f"Get all projects failed: {e}")
        return []
