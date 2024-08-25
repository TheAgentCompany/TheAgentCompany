import os
import subprocess
import requests
import logging


############################# init variable ##################################### 

HOSTNAME = os.getenv('HOSTNAME') or 'ogma.lti.cs.cmu.edu'
GITLAB_PORT = os.getenv('GITLAB_PORT') or '8929'
GITLAB_USER = "root"
GITLAB_URL = f"http://{HOSTNAME}:{GITLAB_PORT}/{GITLAB_USER}"
TEST_REPO_NAME="api-server"
WIKI_REPO_NAME="yufan-test"

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

def execute_command(command):
    process = subprocess.run(command, shell=True, check=True)
    logger.info(process.stdout)
    return

############################# Test function ##################################### 

# test pull repository from the gitlab server
def test_pull_repository():
    execute_command(f"rm -rf {TEST_REPO_NAME}")
    execute_command(f"git clone {GITLAB_URL}/{TEST_REPO_NAME}.git")
    return

# test access wiki document
def test_wiki():
    response = requests.get(f"{GITLAB_URL}/{WIKI_REPO_NAME}/-/wikis/home")
    logger.debug(response.content)
    if "Welcome to Bridges-2" not in str(response.content):
        logger.Error("cannot get correct wiki")
    return

# test access specific internet
# test block specific internet
def can_access_website():
    try:
        response = requests.get('https://www.google.com', timeout=5)
        if response.status_code == 200:
            logger.info("can visit google")
            return True
        else:
            logger.Error("cannot access google")
            return False
    except requests.RequestException as e:
        logger.Error("cannot access google")
        return False

# test mock local API
# test prepared file

if __name__ == "__main__":
    # test_pull_repository()
    # test_wiki()
    can_access_website()