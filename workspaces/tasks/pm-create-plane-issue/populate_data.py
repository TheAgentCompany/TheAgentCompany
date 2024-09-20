import os
import requests
import logging

############################# init variable ##################################### 
HOSTNAME = os.getenv('PLANE_HOSTNAME') or 'ogma.lti.cs.cmu.edu'
PLANE_PORT = os.getenv('PLANE_PORT') or '8091'
PLANE_BASEURL = f"http://{HOSTNAME}:{PLANE_PORT}"
PLANE_WORKSPACE_SLUG = os.getenv("PLANE_WORKSPACE_SLUG") or "tac"
API_KEY = os.getenv('PLANE_API')
headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
}

############################# util function #####################################  
# Set up logging
logging.basicConfig(level=logging.INFO,    
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        # logging.FileHandler("app.log"),  # Log messages to a file
        logging.StreamHandler()  # Log messages to the console
    ])
logger = logging.getLogger("Functionality Test")

############################# Test function ##################################### 

def create_project(project_name, project_identifer):
    """Create a project in plane"""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"

    payload = {
        "name": project_name,
        "identifier": project_identifer,
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    if response.status_code == 201:
        resp = response.json()
        logger.info(f"Project {project_name} create.")
        return resp.get("id")
    else:
        print(response.status_code, url)
        logger.error(f"Failed to create {project_name} project.")
        return False
    
# def create_issue(project_id, issue):
#     """Create an issue in plane"""
#     payload = {"name": issue}
#     url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/issues/"
#     response = requests.request("POST", url, json=payload, headers=headers)
#     if response.status_code == 201:
#         logger.info(f"Successfully created issue")
#         return True
#     else:
#         logger.error(f"Failed to create issue")
#         return False
    
if __name__ == "__main__":
    project_name = "Web Dashboard"
    project_identifer = "wdash"
    project = create_project(project_name, project_identifer)