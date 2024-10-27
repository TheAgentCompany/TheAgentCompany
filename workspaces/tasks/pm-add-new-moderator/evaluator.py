import os
import logging
import json
from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client


SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"

# Create RocketChat instance
rocket = create_rocketchat_client()

def checkpoint1(trajectory):
    return f"{ROCKETCHAT_URL}/home" in trajectory


def checkpoint2(trajectory):
    return f"{ROCKETCHAT_URL}/channel/general" in trajectory


def check_user_role(username, role):
    try:
        roles = rocket.roles_get_users_in_role(role).json()
        users_list = roles.get("users", [])
        return any(user['username'] == username for user in users_list)
    except Exception:
        logging.warning("Fail to check user role", exc_info=True)
        return False


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    checkpoints.append(Checkpoint(1, int(checkpoint1(trajectory))))

    checkpoints.append(Checkpoint(1, int(checkpoint2(trajectory))))

    checkpoints.append(Checkpoint(1, int(check_user_role("kritanjali.jain", "moderator"))))

    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))
