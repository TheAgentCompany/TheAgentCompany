import os
import subprocess
import requests
import logging
from rocketchat_API.rocketchat import RocketChat

############################# init variable ##################################### 
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'ogma.lti.cs.cmu.edu'
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



def find_channel(channel_name):
    """Find the channel in Rocket.Chat."""
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        logger.info(f"Channel #{channel_name} found.")
        return True
    else:
        logger.error(f"Failed to find the #{channel_name} channel.")
        return False

def check_channel_exists(channel_name):
    channels = rocket.channels_list().json()
    channel_names = channels.get("channels")
    return any(current_channel['name'] == channel_name for current_channel in channel_names)

def send_message(channel_name, message):
    """Send a message to the specified channel."""
    response = rocket.chat_post_message(message, channel=f"#{channel_name}").json()
    if response.get('success'):
        logger.info(f"Successfully sent '{message}' to the #{channel_name} channel.")
        return True
    else:
        logger.error(f"Failed to send '{message}' to the #{channel_name} channel.")
        return False

def create_channel(channel_name):
    if check_channel_exists(channel_name) == True:
        logger.info("Channel already exists")
        return False
    response = rocket.channels_create(channel_name).json()
    if response.get('success'):
        logger.info(f"Successfully created '{channel_name}' channel.")
        return True
    else:
        logger.error(f"Failed to create '{channel_name}' channel.")
        return False

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

def check_user_role(username, role):
    roles = rocket.roles_get_users_in_role(role).json()
    users_list = roles.get("users")
    return any(user['username'] == username for user in users_list)


def add_user_role_owner(channel_name, username):
    if check_user_role(username, 'owner') == True:
        logger.info("Role already assigned")
        return False
    response_channel = rocket.channels_info(channel=channel_name).json()
    channel_id = response_channel['channel']['_id']
    response = rocket.channels_add_owner(channel_id, username = username).json()
    if response.get('success'):
        logger.info(f"Successfully assigned {username} as owner.")
        return True
    else:
        logger.error(f"Failed to assign {username} as owner.")
        return False

if __name__ == "__main__":
    channel_name = "general"
    username = 'jobbench'
    print(add_user_role_owner(channel_name, username))

