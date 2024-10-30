"""
Check if there's at least one joined channel and one unjoined channel in Rocket.Chat
"""

import logging

from common import create_rocketchat_client

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

def found_joined_and_unjoined_channels():
    rocket_client = create_rocketchat_client()
    all_channels = rocket_client.channels_list().json().get('channels', [])
    if len(all_channels) == 0:
        raise Exception("no channels found")
    
    joined_channels = rocket_client.channels_list_joined().json().get('channels', [])
    if len(joined_channels) == 0:
        raise Exception("no joined channels found")

    logger.info(f"list of all channels: {str([c['name'] for c in all_channels])}")
    logger.info(f"list of joined channels: {str([c['name'] for c in joined_channels])}")
    if len(all_channels) == len(joined_channels):
        raise Exception("no unjoined channels found")
    
    return


if __name__ == "__main__":
    found_joined_and_unjoined_channels()
