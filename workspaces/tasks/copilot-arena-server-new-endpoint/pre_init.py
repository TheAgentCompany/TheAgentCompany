import os
import subprocess
import logging


############################# init variable #####################################

SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME") or "ogma.lti.cs.cmu.edu"
GITLAB_PORT = os.getenv("GITLAB_PORT") or "8929"
GITLAB_USER = "root"
GITLAB_URL = f"http://{SERVER_HOSTNAME}:{GITLAB_PORT}/{GITLAB_USER}"
TEST_REPO_NAME = "copilot-arena-server"

############################# util function #####################################
# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        # logging.FileHandler("app.log"),  # Log messages to a file
        logging.StreamHandler()  # Log messages to the console
    ],
)
logger = logging.getLogger("Functionality Test")


def execute_command(command):
    process = subprocess.run(command, shell=True, check=True)
    logger.info(process.stdout)
    return


# pull repository from the gitlab server
def pull_repository():
    execute_command(f"rm -rf {TEST_REPO_NAME}")
    execute_command(f"git clone {GITLAB_URL}/{TEST_REPO_NAME}.git")
    return


if __name__ == "__main__":
    pull_repository()
