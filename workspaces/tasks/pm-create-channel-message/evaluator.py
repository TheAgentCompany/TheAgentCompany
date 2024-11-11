import os

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client, checkpoint

# Rocket.Chat server URL and admin credentials
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"


# Create RocketChat instance
rocket = create_rocketchat_client()

@checkpoint
def grade_checkpoint1(trajectory):
    return f"{ROCKETCHAT_URL}/home" in trajectory


def get_channel_room_id(channel_name):
    """Get the room_id for a specific channel by its name."""
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

@checkpoint
def check_user_added(channel_name, username):
    room_id = get_channel_room_id(channel_name)
    if not room_id:
        print(f"Failed to find room ID for channel #{channel_name}.")
        return False
    members = rocket.channels_members(channel=channel_name).json()
    users_list = members.get("members", [])
    return any(user['username'] == username for user in users_list)

@checkpoint
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


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))

    checkpoints.append(Checkpoint(1, int(check_user_added("finance-talk", "david_wong"))))

    checkpoints.append(Checkpoint(1, int(check_message_sent("finance-talk", "Welcome to the finance-talk channel!", "theagentcompany"))))

    return result



