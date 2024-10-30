import requests
import logging
from config import PLANE_BASEURL, PLANE_WORKSPACE_SLUG, PLANE_HEADERS

############################# Logging Setup #####################################  
# Set up logging
logging.basicConfig(level=logging.INFO,    
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        # logging.FileHandler("app.log"),  # Log messages to a file
        logging.StreamHandler()  # Log messages to the console
    ])
logger = logging.getLogger("Functionality Test")

############################# Utility Functions ##################################### 

def create_issues_in_gitlab():
    return


if __name__ == "__main__":
    # Create issues in GitLab
    create_issues_in_gitlab()