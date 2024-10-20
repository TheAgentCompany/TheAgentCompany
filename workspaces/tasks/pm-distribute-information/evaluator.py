import os
from rocketchat_API.rocketchat import RocketChat

import sys
import logging

############################# Init Variables #####################################
# Rocket.Chat variables
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'the-agent-company.com'


ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'

ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASS = 'jobbench'

GITLAB_PORT = os.getenv('GITLAB_PORT') or '8929'
GITLAB_USER = "root"
GITLAB_URL = f"http://{SERVER_HOSTNAME}:{GITLAB_PORT}/{GITLAB_USER}"

# Initialize RocketChat client
rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASS, server_url=ROCKETCHAT_URL)

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
        msgs = rocket.im_history(room_id=member['_id']).json()['messages']
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

def evaluate(trajectory):
    points = 0

    if check_trajectory(trajectory):
        print("bathtub issue accessed")
        points += 1
    else:
        print("bathtub issue not accessed")

    if check_project_distributed():
        points += 1

    print(f"Evaluation completed. Final score: {points}/2")
    return points

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.warning("No trajectory file provided, assuming empty trajectory")
        trajectory = ""
    else:
        trajectory = load_trajectory(sys.argv[1])

    evaluate(trajectory)
