import logging
from config import GITLAB_USER
from common import make_gitlab_request

GITLAB_PROJECT_PATH=f"{GITLAB_USER}/risingwave"

MILESTONE = "Alpha Release"
ISSUE_1 = 'Implement stream processing engine'
ISSUE_2 = 'Integrate with Kafka'

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

def create_milestone_in_gitlab():
    milestone_exists = False
    milestone = make_gitlab_request(GITLAB_PROJECT_PATH, "milestones")
    milestone_exists = MILESTONE in [milestone["title"] for milestone in milestone.json()]
    if not milestone_exists:
        logger.info("Creating milestone in Gitlab")
        make_gitlab_request(GITLAB_PROJECT_PATH, "milestones", method = "POST", params={"title": MILESTONE})
    return

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
        make_gitlab_request(GITLAB_PROJECT_PATH, "issues", method = "POST", params={"title": ISSUE_2})
    return

if __name__ == "__main__":
    create_milestone_in_gitlab()
    create_issues_in_gitlab()