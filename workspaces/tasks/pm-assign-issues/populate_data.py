import os
import requests
import logging
from rocketchat_API.rocketchat import RocketChat

############################# Initialization Variables #####################################
HOSTNAME = os.getenv('HOSTNAME') or 'ogma.lti.cs.cmu.edu'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
CHANNEL_NAME = "sprint-planning"
ROCKETCHAT_URL = f"http://{HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASS = 'jobbench'

# Initialize the RocketChat client with username and password
rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASS, server_url=ROCKETCHAT_URL)

############################# Logging Setup #####################################  
logging.basicConfig(level=logging.INFO,    
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()  # Log messages to the console
    ])
logger = logging.getLogger("Data Population")

############################# Utility Functions ##################################### 

def create_channel(channel_name):
    response = rocket.channels_create(channel_name).json()
    if response.get('success'):
        logger.info(f"Successfully created channel {channel_name}.")
        return response['channel']['_id']
    else:
        logger.error(f"Failed to create channel {channel_name}: {response.get('error')}")
        return None

def post_message(user_credentials, channel_id, message):
    user_rocket = RocketChat(user_credentials['username'], user_credentials['password'], server_url=ROCKETCHAT_URL)
    response = user_rocket.chat_post_message(message, room_id=channel_id).json()
    if response.get('success'):
        logger.info(f"Message posted to channel by {user_credentials['username']}.")
    else:
        logger.error(f"Failed to post message by {user_credentials['username']}: {response.get('error')}")

def add_user_to_channel(channel_id, username):
    """Add a user to the specified channel using the user ID."""
    # Get user info to fetch the user_id
    user_info = rocket.users_info(username=username).json()
    
    if user_info.get('success'):
        user_id = user_info['user']['_id']
        # Invite user to the channel using user_id
        response = rocket.channels_invite(room_id=channel_id, user_id=user_id).json()
        
        if response.get('success'):
            logger.info(f"Successfully added {username} to the channel.")
        else:
            logger.error(f"Failed to add {username} to the channel: {response.get('error')}")
    else:
        logger.error(f"Failed to get info for user {username}: {user_info.get('error')}")

def user_exists(username):
    """Check if a user exists in RocketChat."""
    response = rocket.users_info(username=username).json()
    if response.get('success'):
        logger.info(f"User {username} already exists.")
        return True
    else:
        logger.info(f"User {username} does not exist.")
        return False


def setup_user(user_name, password, email, username):
    # Check if user already exists
    if user_exists(username):
        return {'username': username, 'password': password}
    response = rocket.users_create(email, user_name, password, username).json()
    if response.get('success'):
        logger.info(f"Successfully created user {username}.")
        return {'username': username, 'password': password}
    else:
        logger.error(f"Failed to create user {username}: {response.get('error')}")
        return None

############################# Population Script ##################################### 


def populate_channel():
    # Create the sprint-planning channel
    channel_id = create_channel(CHANNEL_NAME)
    if not channel_id:
        return

    # Define user credentials
    users = [
        {'name': 'Kritanjali Jain', 'password': 'cmu@', 'email': 'ksjain@agent.com', 'username': 'kritanjali.jain'},
        {'name': 'John Doe', 'password': 'John.Doe', 'email': 'John.Doe@cmu.edu.com', 'username': 'John.Doe'},
        {'name': 'Rocket Cat', 'password': 'jobbench', 'email': 'rocket.Cat@email.com', 'username': 'rocket.cat'}
    ]

    user_credentials_list = []

    # First, set up users and add them to the channel
    for user in users:
        user_credentials = setup_user(user['name'], user['password'], user['email'], user['username'])
        if user_credentials:
            user_credentials_list.append(user_credentials)
            # Add user to the 'sprint-planning' channel
            add_user_to_channel(channel_id, user['username'])

    # Then, send messages after all users have been added to the channel
    for user_credentials in user_credentials_list:
        if user_credentials['username'] == 'kritanjali.jain':
            post_message(user_credentials, channel_id, "Okay, for this sprint, I think we should focus on the frontend. We need to update the navigation bar. I can take that, but I think I'll need about 5 days to finish it.")
        elif user_credentials['username'] == 'John.Doe':
            post_message(user_credentials, channel_id, "I agree with that. On my side, I'll be working on setting up the backend API for the payment processing. I estimate it will take me around 10 days. Let me know if anyone can assist with this if needed.")
        elif user_credentials['username'] == 'rocket.cat':
            post_message(user_credentials, channel_id, "I'll handle the unit tests for the authentication service. I think 7 days is enough time for that.")

if __name__ == "__main__":
    populate_channel()
