import os
from rocketchat_API.rocketchat import RocketChat

import datetime

# Set environment variables
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'theagentcompany.com'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'

# Construct RocketChat URL
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"

# Set admin credentials
ADMIN_USERNAME = 'jobbench'
ADMIN_PASSWORD = 'jobbench'

# Create RocketChat instance
rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASSWORD, server_url=ROCKETCHAT_URL)


def get_history(username):
    id = ""
    for item in rocket.users_list().json()['users']:
        if item['username'] == username:
            id = item["_id"]
            break
    msgs = rocket.im_history(room_id=id).json()['messages']
    for msg in msgs[::-1]:
        print(f"{username}'s chat: {msg['msg']}")

    return msgs

def checkpoint1(content: str):
    return content is not None and len(content) > 0

def checkpoint2(content: str):
    if content is None or len(content) == 0:
        return False
    return 'coke' in content and 'dew' in content

def checkpoint3(content: str):
    if content is None or len(content) == 0:
        return False
    return 'apple' in content and 'sprite' in content

def calculate_total_score():
    scores = {
        checkpoint1: 1,
        checkpoint2: 1,
        checkpoint3: 1,
    }

    total_score = 0

    msgs = get_history(username='chen_xinyi')
    content = ""
    for msg in msgs[::-1]:
        content += msg['msg'].lower()

    for func, score in scores.items():
        if func(content):
            total_score += score

    return total_score

# compute the total point
total = calculate_total_score()
print(f"\ntotal points: {total}")