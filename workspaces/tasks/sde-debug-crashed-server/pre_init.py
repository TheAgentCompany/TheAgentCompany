import os
import subprocess
import requests
import logging


############################# init variable ##################################### 

SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'ogma.lti.cs.cmu.edu'
NEXCTCLOUD_PORT = os.getenv('NEXCTCLOUD_PORT') or '80'
NEXCTCLOUD_URL = f"http://{SERVER_HOSTNAME}:{NEXCTCLOUD_PORT}"

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
################### Please delete the test you don't need #######################

# test access file document
def test_file():
    response = requests.get(f"{NEXCTCLOUD_URL}/apps/files/files/626?dir=/Documents/Financials")
    logger.debug(response.content)
    if "July-September 2024 Financials.ods" not in str(response.content):
        logger.Error("cannot get correct file")
    return



if __name__ == "__main__":
    test_file()
    