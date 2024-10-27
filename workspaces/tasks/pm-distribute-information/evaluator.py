import os
import logging
import json
from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final


############################# Init Variables #####################################
# Rocket.Chat variables
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'


ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'

ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"

GITLAB_PORT = os.getenv('GITLAB_PORT') or '8929'
GITLAB_USER = "root"
GITLAB_URL = f"http://{SERVER_HOSTNAME}:{GITLAB_PORT}/{GITLAB_USER}"

from common import create_rocketchat_client

# Create RocketChat instance
rocket = create_rocketchat_client()

############################# Helper Functions #####################################

def check_trajectory(trajectory):
    return f"{GITLAB_URL}/bustub/-/issues/759" in trajectory

def get_database_members(channel_name=["project-graphdb", "project-streamdb"]):

    members = []

    for channel in channel_name:
        members_response = rocket.channels_members(channel=channel).json()
        members_in_c = members_response.get("members", [])
        members.extend(members_in_c)

    return members


def check_project_distributed():
    members = get_database_members()

    for member in members:
        msgs = rocket.im_history(room_id=member['_id']).json().get('messages', [])
        msg_log = ""
        for msg in msgs[::-1]:
            print(f"{member['username']}'s chat: {msg['msg']}")
            msg_log += msg['msg']
            msg_log += "\n"
        if "http://the-agent-company.com:8929/root/bustub/-/issues/759" not in msg_log:
            return False

    return True


def load_trajectory(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except Exception as e:
        logging.warning(f"Error reading trajectory file: {e}")
        return ""

############################# Evaluator #####################################


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)
    checkpoints.append(Checkpoint(1, int(check_trajectory(trajectory))))
    checkpoints.append(Checkpoint(1, check_project_distributed()))
    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))