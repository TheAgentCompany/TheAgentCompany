import os
import logging

from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client

# Create RocketChat instance
rocket = create_rocketchat_client()

def check_url(trajectory):
    return f"channel/general" in trajectory


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


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    checkpoints.append(Checkpoint(1, check_url(trajectory)))
    checkpoints.append(Checkpoint(1, check_message_sent("general", "Hi", "theagentcompany")))
    return result



