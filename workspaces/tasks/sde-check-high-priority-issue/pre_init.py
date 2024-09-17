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

def add_user_to_channel(channel_name, username):
    response_user = rocket.users_info(username = username).json()
    user_id = response_user['user']['_id']
    response_channel = rocket.channels_info(channel=channel_name).json()
    channel_id = response_channel['channel']['_id']
    response = rocket.channels_invite(channel_id, user_id).json()
    if response.get('success'):
        logger.info(f"Successfully added {username} to '{channel_name}'.")
        return True
    else:
        logger.error(f"Failed to add {username}  to '{channel_name}' channel.")
        return False

if __name__ == "__main__":
    channel_name = "Janusgraph"
    username = 'Colby.Devin'
    print(add_user_to_channel(channel_name, username))
