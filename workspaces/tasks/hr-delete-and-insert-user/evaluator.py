
from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client, checkpoint

# Create RocketChat instance
rocket = create_rocketchat_client()

def check_user_added(channel_name, username):
    members = rocket.channels_members(channel=channel_name).json()
    users_list = members.get("members", [])
    return any(user['username'] == username for user in users_list)

def check_user_removed(username):
    response_user = rocket.users_info(username=username).json()
    is_exist = response_user.get('success', False)
    return not is_exist

def check_user_exist(username):
    response_user = rocket.users_info(username=username).json()
    is_exist = response_user.get('success', False)
    return is_exist

@checkpoint
def grade_checkpoint1(username='li_ming'):
    return check_user_removed(username=username)

@checkpoint
def grade_checkpoint2(username='dandan_liu'):
    return check_user_exist(username=username)

@checkpoint
def grade_checkpoint3(channel_name='product', username='dandan_liu'):
    return check_user_added(channel_name=channel_name,username=username)

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Define the scores corresponding to when each function is True
    scores = {
        grade_checkpoint1: 1,
        grade_checkpoint2: 1,
        grade_checkpoint3: 1
    }

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func())))

    return result



