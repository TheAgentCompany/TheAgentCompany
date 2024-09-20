import requests
import os
from rocketchat_API.rocketchat import RocketChat
import ipdb

# Rocket.Chat server URL and admin credentials
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'ogma.lti.cs.cmu.edu'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
channel_name = "general"
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASS = 'jobbench'

# Initialize the RocketChat client with username and password
rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASS, server_url=ROCKETCHAT_URL)

def check_url_1(browser_logs):
    return f"{ROCKETCHAT_URL}/home" in browser_logs

def check_url_2(browser_logs):
    return f"{ROCKETCHAT_URL}/channel/webagents" in browser_logs

def get_channel_room_id(channel_name):
    """Get the room_id for a specific channel by its name."""
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

def check_channel_exists(channel_name):
    channels = rocket.channels_list().json()
    channel_names = channels.get("channels")
    return any(current_channel['name'] == channel_name for current_channel in channel_names)

def check_user_added(channel_name, username):
    room_id = get_channel_room_id(channel_name)
    if not room_id:
        print(f"Failed to find room ID for channel #{channel_name}.")
        return False
    members = rocket.channels_members(channel=channel_name).json()
    users_list = members.get("members")
    return any(user['username'] == username for user in users_list)


def check_message_sent(channel_name, message, username):
    room_id = get_channel_room_id(channel_name)
    if not room_id:
        print(f"Failed to find room ID for channel #{channel_name}.")
        return False

    # Fetch message history for the channel using room_id (channel_id)
    response = rocket.channels_history(room_id=room_id).json()

    if response.get('success'):
        messages = response.get('messages', [])
        # Check if the message 'Hi' is in the most recent messages from a specific user
        for msg in messages:
            if msg.get('msg') == message and msg.get('u', {}).get('username') == username:
                return True
    return False


if __name__ == "__main__":
    test_url_1 = f"{ROCKETCHAT_URL}/home"
    print(check_url_1(f"ACTION: goto('{test_url_1}')"))
    print(check_channel_exists("webagents"))
    test_url_2 = f"{ROCKETCHAT_URL}/channel/webagents"
    print(check_url_2(f"ACTION: goto('{test_url_2}')"))
    print(check_user_added("webagents", "kritanjali.jain"))
    print(check_message_sent("webagents", "Welcome to the webagents channel!", "jobbench"))

