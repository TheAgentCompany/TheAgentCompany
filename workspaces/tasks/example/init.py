"""
This is boilerplate code that does initialization work to set up the exam environment.
"""

import os
import logging


############################# init variable ##################################### 

HOSTNAME = os.getenv('HOSTNAME') or 'ogma.lti.cs.cmu.edu'
GITLAB_PORT = os.getenv('GITLAB_PORT') or '8929'
GITLAB_USER = "root"
GITLAB_URL = f"http://{HOSTNAME}:{GITLAB_PORT}/{GITLAB_USER}"
TEST_REPO_NAME="api-server"
WIKI_REPO_NAME="wiki-test"

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
