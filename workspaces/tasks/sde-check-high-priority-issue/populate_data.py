# You should do the initialization work in this python file to set up the environment you need
import os
import subprocess
import requests
import logging
from rocketchat_API.rocketchat import RocketChat

############################# init variable ##################################### 
HOSTNAME = os.getenv('HOSTNAME') or 'ogma.lti.cs.cmu.edu'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
CHANNEL_NAME = "general"
ROCKETCHAT_URL = f"http://{HOSTNAME}:{ROCKETCHAT_PORT}"
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

def create_user():
    user_name = "Colby Devin"
    user_password = 'Colby@Devin'
    user_email = 'Colby.Devin@andrew.cmu.edu'
    user_username = 'Colby.Devin'
    response = rocket.users_create(user_email,user_name,user_password, user_username).json()
    if response.get('success'):
        logger.info(f"Successfully created user.")
        return True
    else:
        logger.error(f"{response.get('error')}")
        return False


def check_channel_exists(channel_name):
    channels = rocket.channels_list().json()
    channel_names = channels.get("channels")
    return any(current_channel['name'] == channel_name for current_channel in channel_names)


def create_channel(channel_name):
    if check_channel_exists(channel_name) == True:
        logger.info("Channel already exists")
        return False
    response = rocket.channels_create(channel_name).json()
    if response.get('success'):
        logger.info(f"Successfully created channel.")
        return True
    else:
        logger.error(f"{response.get('error')}")
        return False

if __name__ == "__main__":
    create_channel("Janusgraph")
    create_user()