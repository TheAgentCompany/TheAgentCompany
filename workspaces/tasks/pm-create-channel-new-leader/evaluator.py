
from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client, checkpoint


# Create RocketChat instance
rocket = create_rocketchat_client()

@checkpoint
def checkpoint1(trajectory):
    return f"home" in trajectory

@checkpoint
def check_channel_exists(channel_name):
    channels = rocket.channels_list().json()
    channel_names = channels.get("channels", [])
    return any(current_channel['name'] == channel_name for current_channel in channel_names)

@checkpoint
def check_user_role(username, role):
    roles = rocket.roles_get_users_in_role(role).json()
    users_list = roles.get("users", [])
    return any(user['username'] == username for user in users_list)


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    checkpoints.append(Checkpoint(1, int(checkpoint1(trajectory))))

    checkpoints.append(Checkpoint(1, int(check_channel_exists("sales-talk"))))

    checkpoints.append(Checkpoint(1, int(check_user_role("mark_johnson", "leader"))))

    return result


