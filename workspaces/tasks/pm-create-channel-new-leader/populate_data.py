# You should do the initialization work in this python file to set up the environment you need
import os
import subprocess
import requests
import logging
from rocketchat_API.rocketchat import RocketChat


############################# init variable ##################################### 
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
CHANNEL_NAME = "general"
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASS = 'jobbench'

# Initialize the RocketChat client with username and password
rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASS, server_url=ROCKETCHAT_URL)

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

def execute_command(command):
    process = subprocess.run(command, shell=True, check=True)
    logger.info(process.stdout)
    return

def populate_data():
    user_name = "Kritanjali Jain"
    user_password = 'hello'
    user_email = 'spoof123@gmail.com'
    user_username = 'kritanjali.jain'
    response = rocket.users_create(user_email,user_name,user_password, user_username).json()
    if response.get('success'):
        logger.info(f"Successfully created user.")
        return True
    else:
        logger.error(f"{response.get('error')}")
        return False

if __name__ == "__main__":
    populate_data()