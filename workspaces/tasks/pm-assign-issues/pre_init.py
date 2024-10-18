import os
from rocketchat_API.rocketchat import RocketChat

############################# Init Variables #####################################
HOSTNAME =  'theagentcompany.com'
ROCKETCHAT_PORT =  '3000'
CHANNEL_NAME = "sprint-planning"
ROCKETCHAT_URL = f"http://{HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASS = 'jobbench'

# Initialize the RocketChat client with admin username and password
rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASS, server_url=ROCKETCHAT_URL)

############################# Helper Functions #####################################

def check_channel_exists(channel_name):
    """Check if the specified channel exists."""
    response = rocket.channels_list().json()
    channels = response.get("channels", [])
    return any(channel['name'] == channel_name for channel in channels)

def get_channel_room_id(channel_name):
    """Get the room_id for a specific channel by its name."""
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

def check_user_added(channel_name, username):
    """Check if a user is a member of a specific channel."""
    room_id = get_channel_room_id(channel_name)
    if not room_id:
        print(f"Failed to find room ID for channel #{channel_name}.")
        return False
    members_response = rocket.channels_members(channel=channel_name).json()
    members = members_response.get("members", [])
    return any(member['username'] == username for member in members)

############################# Pre-Initialization Tests #####################################

def pre_init_checks():
    # Check if the 'sprint-planning' channel exists
    if not check_channel_exists(CHANNEL_NAME):
        print(f"Channel '{CHANNEL_NAME}' does not exist.")
        return False
    else:
        print(f"Channel '{CHANNEL_NAME}' exists.")

    # Check if kritanjali.jain is added to the channel
    if not check_user_added(CHANNEL_NAME, 'kritanjali.jain'):
        print("User 'kritanjali.jain' is not added to the channel.")
        return False
    else:
        print("User 'kritanjali.jain' is added to the channel.")

    # Check if john.doe is added to the channel
    if not check_user_added(CHANNEL_NAME, 'John.Doe'):
        print("User 'john.doe' is not added to the channel.")
        return False
    else:
        print("User 'john.doe' is added to the channel.")

    # Check if rocket.cat is added to the channel
    if not check_user_added(CHANNEL_NAME, 'rocket.cat'):
        print("User 'rocket.cat' is not added to the channel.")
        return False
    else:
        print("User 'rocket.cat' is added to the channel.")

    return True

if __name__ == "__main__":
    if pre_init_checks():
        print("Pre-initialization checks passed.")
    else:
        print("Pre-initialization checks failed.")
