import os
import subprocess
import requests
import logging


############################# init variable ##################################### 

SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
GITLAB_PORT = os.getenv('GITLAB_PORT') or '8929'
GITLAB_USER = "root"
GITLAB_URL = f"http://{SERVER_HOSTNAME}:{GITLAB_PORT}/{GITLAB_USER}"
TEST_REPO_NAME="api-server"

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


# test block specific internet
def can_access_website(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            logger.info(f"can visit {url}")
            return True
        else:
            logger.error(f"cannot access {url}")
            return False
    except requests.RequestException as e:
        logger.Error(f"cannot access {url}")
        return False

# test mock local API
# test prepared file

if __name__ == "__main__":
    pass
    # test_pull_repository()
    # can_access_website("https://www.pexels.com/photo/a-bee-is-on-a-sunflower-in-a-field-27220813/")