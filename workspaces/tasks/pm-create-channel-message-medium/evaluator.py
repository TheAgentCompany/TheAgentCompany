import os

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client

# Rocket.Chat server URL and admin credentials
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"

# Create RocketChat instance
rocket = create_rocketchat_client()

def get_channel_room_id(channel_name):
    """Get the room_id for a specific channel by its name."""
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

def check_channel_exists(channel_name):
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        return True
    return False

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

def grade_checkpoint1(trajectory):
    return f"{ROCKETCHAT_URL}/home" in trajectory

def grade_checkpoint3(trajectory):
    return f"{ROCKETCHAT_URL}/channel/literaturereview" in trajectory

def grade_checkpoint5(trajectory):
    return f"{ROCKETCHAT_URL}/channel/benchmarking" in trajectory

def grade_checkpoint2():
    return check_channel_exists("literaturereview")

def grade_checkpoint4():
    return check_channel_exists("benchmarking")

def grade_checkpoint6():
    return check_user_added("literaturereview", "emma_lewis")

def grade_checkpoint7():
    return check_user_added("literaturereview", "wang_fang")

def grade_checkpoint9():
    return check_user_added("benchmarking", "emma_lewis")

def grade_checkpoint10():
    return check_user_added("benchmarking", "alex_turner")

def grade_checkpoint11():
    return check_user_added("benchmarking", "david_wong")

def grade_checkpoint8():
    return check_message_sent("literaturereview", 'Welcome to the literature review channel!', "theagentcompany")

def grade_checkpoint12():
    return check_message_sent("benchmarking", 'This will be for all our benchmarking projects.', "theagentcompany")

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, 1 * int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, 1 * int(passed2)))

    passed3 = grade_checkpoint3(trajectory)
    checkpoints.append(Checkpoint(1, 1 * int(passed3)))

    passed4 = grade_checkpoint4()
    checkpoints.append(Checkpoint(1, 1 * int(passed4)))

    passed5 = grade_checkpoint5(trajectory)
    checkpoints.append(Checkpoint(1, 1 * int(passed5)))

    passed6 = grade_checkpoint6()
    checkpoints.append(Checkpoint(1, 1 * int(passed6)))

    passed7 = grade_checkpoint7()
    checkpoints.append(Checkpoint(1, 1 * int(passed7)))

    passed8 = grade_checkpoint8()
    checkpoints.append(Checkpoint(1, 1 * int(passed8)))

    passed9 = grade_checkpoint9()
    checkpoints.append(Checkpoint(1, 1 * int(passed9)))

    passed10 = grade_checkpoint10()
    checkpoints.append(Checkpoint(1, 1 * int(passed10)))

    passed11 = grade_checkpoint11()
    checkpoints.append(Checkpoint(1, 1 * int(passed11)))

    passed12 = grade_checkpoint12()
    checkpoints.append(Checkpoint(1, 1 * int(passed12)))

    return result
