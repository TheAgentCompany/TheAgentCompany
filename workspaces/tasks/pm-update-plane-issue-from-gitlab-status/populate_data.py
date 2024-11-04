import logging
from config import GITLAB_USER
from common import create_plane_issue, get_plane_issue_details, get_plane_cycle_details, add_plane_issue_to_cycle, get_plane_project_id, make_gitlab_request

GITLAB_PROJECT_PATH=f"{GITLAB_USER}/janusgraph"

PLANE_PROJECT_NAME = "JanusGraph"
PLANE_PROJECT_ID = get_plane_project_id(PLANE_PROJECT_NAME)
CYCLE_NAME = "Sprint 1"
ISSUE_1 = "Improve Logging for Bulk Request Failures"
ISSUE_2 = "Optimize Retry Mechanism for Out of Memory Errors"

############################# Logging Setup #####################################  
# Set up logging
logging.basicConfig(level=logging.INFO,    
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()  # Log messages to the console
    ])
logger = logging.getLogger("Functionality Test")

############################# Utility Functions ##################################### 

def create_issues_in_gitlab():
    issue1_exists = False
    issue1 = make_gitlab_request(GITLAB_PROJECT_PATH, "issues")
    issue1_exists = ISSUE_1 in [issue["title"] for issue in issue1.json()]
    if not issue1_exists:
        logger.info("Creating issue 1 in Gitlab")
        make_gitlab_request(GITLAB_PROJECT_PATH, "issues", method = "POST", params={"title": ISSUE_1})

    issue2_exists = False
    issue2 = make_gitlab_request(GITLAB_PROJECT_PATH, "issues")
    issue2_exists = ISSUE_2 in [issue["title"] for issue in issue2.json()]
    if not issue2_exists:
        logger.info("Creating issue 2 in Gitlab")
        issue2_response = make_gitlab_request(GITLAB_PROJECT_PATH, "issues", method = "POST", params={"title": ISSUE_2})
        if issue2_response.status_code != 201:
            logger.error(f"Failed to create issue 2 in Gitlab: {issue2_response.text}")
        issue2_id = issue2_response.json()["iid"]
        make_gitlab_request(GITLAB_PROJECT_PATH, f"issues/{issue2_id}?state_event=close", method = "PUT")
    return

def create_issues_in_plane():
    cycle = get_plane_cycle_details(PLANE_PROJECT_ID, CYCLE_NAME)
    issue1 = get_plane_issue_details(PLANE_PROJECT_ID, ISSUE_1)
    if issue1 is None:
        logger.info("Creating issue 1 in Plane")
        create_plane_issue(PLANE_PROJECT_ID, ISSUE_1)
        issue1 = get_plane_issue_details(PLANE_PROJECT_ID, ISSUE_1)
        add_plane_issue_to_cycle(PLANE_PROJECT_ID, cycle["id"], issue1["id"])

    issue2 = get_plane_issue_details(PLANE_PROJECT_ID, ISSUE_2)
    if issue2 is None:
        logger.info("Creating issue 2 in Plane")
        create_plane_issue(PLANE_PROJECT_ID, ISSUE_2)
        issue2 = get_plane_issue_details(PLANE_PROJECT_ID, ISSUE_2)
        add_plane_issue_to_cycle(PLANE_PROJECT_ID, cycle["id"], issue2["id"])
    return

if __name__ == "__main__":
    create_issues_in_plane()
    create_issues_in_gitlab()