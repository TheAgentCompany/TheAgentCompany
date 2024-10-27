import os
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

def check_api_sanity():
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    response = requests.request("GET", url, headers=PLANE_HEADERS)
    if response.status_code != 200:
        logger.error("Invalid API Key / Workspace")

if __name__ == "__main__":
    check_api_sanity()

