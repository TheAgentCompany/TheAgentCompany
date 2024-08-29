import os
import subprocess
import requests
import logging

############################# init variable ##################################### 
HOSTNAME = 'ogma.lti.cs.cmu.edu'
ROCKETCHAT_PORT = '3000'
CHANNEL_NAME = "general"
ROCKETCHAT_URL = f"http://{HOSTNAME}:{ROCKETCHAT_PORT}"

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

def get_headers():
    """Function to get headers required for API requests."""
    token = os.getenv('ROCKETCHAT_AUTH_TOKEN') or 'vn_Tadey_p7fHnMExAIpgwxFKjpsW4j4-kCpdmB3epq'
    user_id = os.getenv('ROCKETCHAT_USER_ID') or 'qgyxXGaG3uzLq7gDt'
    return {
        'X-Auth-Token': token,
        'X-User-Id': user_id,
        'Content-type': 'application/json',
    }

############################# Test function ##################################### 

def find_channel():
    """Find the #general channel in Rocket.Chat."""
    response = requests.get(f"{ROCKETCHAT_URL}/api/v1/directory", headers=get_headers())
    if response.status_code == 200:
        logger.info("Successfully accessed the channel directory.")
        return True
    else:
        logger.error("Failed to access the channel directory.")
        return False

def send_message(channel_name, message):
    """Send a 'Hi' message to the #general channel."""
    response = requests.post(
        f"{ROCKETCHAT_URL}/api/v1/chat.postMessage",
        headers=get_headers(),
        json={"channel": f"#{channel_name}", "text": message}
    )
    if response.status_code == 200:
        logger.info(f"Successfully sent '{message}' to the #{channel_name} channel.")
        return True
    else:
        logger.error(f"Failed to send '{message}' to the #{channel_name} channel.")
        return False

if __name__ == "__main__":
    if find_channel():
        send_message(CHANNEL_NAME, "Hi")