import requests
import os
from rocketchat_API.rocketchat import RocketChat

# Rocket.Chat server URL and admin credentials
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
channel_name = "general"
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"

from common import create_rocketchat_client

# Create RocketChat instance
rocket = create_rocketchat_client()

def check_url(browser_logs):
    return f"{ROCKETCHAT_URL}/channel/general" in browser_logs


def get_channel_room_id(channel_name):
    """Get the room_id for a specific channel by its name."""
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

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
    test_url = f"{ROCKETCHAT_URL}/channel/general"
    print(check_url(f"ACTION: goto('{test_url}')"))
    print(check_message_sent("general", "Hi", "theagentcompany"))
