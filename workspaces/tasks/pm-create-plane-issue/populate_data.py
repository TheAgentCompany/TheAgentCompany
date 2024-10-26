import requests
import logging
from config import *

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

    response = requests.request("POST", url, json=payload, headers=PLANE_HEADERS)
    if response.status_code == 201:
        resp = response.json()
        logger.info(f"Project {project_name} create.")
        return resp.get("id")
    else:
        print(response.status_code, url)
        logger.error(f"Failed to create {project_name} project.")
        return False
    
if __name__ == "__main__":
    project_name = "Web Dashboard"
    project_identifer = "wdash"
    project = create_project(project_name, project_identifer)