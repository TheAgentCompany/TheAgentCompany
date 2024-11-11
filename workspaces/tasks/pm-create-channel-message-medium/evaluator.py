import os
import logging

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import get_rocketchat_channel_room_id, check_rocketchat_message_posted,create_rocketchat_client

# Create RocketChat instance
rocket = create_rocketchat_client()


def check_channel_exists(channel_name):
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        return True
    return False

def check_user_added(rocket_client, channel_name, username):
    room_id = get_rocketchat_channel_room_id(rocket_client, channel_name)
    if not room_id:
        logging.warning(f"Failed to find room ID for channel #{channel_name}.")
        return False
    members = rocket.channels_members(channel=channel_name).json()
    users_list = members.get("members")
    return any(user['username'] == username for user in users_list)


def grade_checkpoint1():
    return check_channel_exists("literaturereview")

def grade_checkpoint4():
    return check_channel_exists("benchmarking")

def grade_checkpoint2():
    return check_user_added(rocket, "literaturereview", "emma_lewis") and check_user_added(rocket, "literaturereview", "wang_fang") and check_user_added(rocket, "benchmarking", "emma_lewis")

def grade_checkpoint5():
    return check_user_added(rocket, "benchmarking", "emma_lewis") and check_user_added(rocket, "benchmarking", "alex_turner") and check_user_added(rocket, "benchmarking", "david_wong")

def grade_checkpoint3():
    return check_rocketchat_message_posted(rocket, "literaturereview", ['Welcome to the literature review channel!'])

def grade_checkpoint6():
    return check_rocketchat_message_posted(rocket, "benchmarking", ['This will be for all our benchmarking projects.'])

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, 1 * int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, 1 * int(passed2)))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(1, 1 * int(passed3)))

    passed4 = grade_checkpoint4()
    checkpoints.append(Checkpoint(1, 1 * int(passed4)))

    passed5 = grade_checkpoint5()
    checkpoints.append(Checkpoint(1, 1 * int(passed5)))

    passed6 = grade_checkpoint6()
    checkpoints.append(Checkpoint(1, 1 * int(passed6)))

    return result
