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

from common import create_rocketchat_client

# Create RocketChat instance
rocket = create_rocketchat_client()

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


def send_message(channel_name, message):
    """Send a message to the specified channel."""
    response = rocket.chat_post_message(message, channel=f"#{channel_name}").json()
    if response.get('success'):
        logger.info(f"Successfully sent '{message}' to the #{channel_name} channel.")
        return True
    else:
        logger.error(f"Failed to send '{message}' to the #{channel_name} channel.")
        return False

if __name__ == "__main__":
    channel_name = "general"
    # Uncomment below while testing not initilisation
    # if find_channel(channel_name):
    #     send_message(channel_name, "Hi")
