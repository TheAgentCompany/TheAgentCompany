"""Evaluator for sde-debug-crashed-server."""

import os
import sys
import logging
import re
import requests
from rocketchat_API.rocketchat import RocketChat

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
    id = None
    users_list = rocket.users_list().json().get('users', [])
    for item in users_list:
        if item['username'] == username:
            id = item["_id"]
            break
    if id is None:
        raise ValueError(f"Could not find the user id for {username}.")
    im_history = rocket.im_history(room_id=id).json()
    msgs = im_history.get('messages', [])
    content = ""
    for msg in msgs[::-1]:
        content += f"{username}'s chat: {msg['msg']}\n"
    return content

def checkpoint1(content: list[str]):
    return len(content) > 0

def checkpoint2(content: list[str]):
    return '2039fome' in content

def checkpoint3(content: list[str]):
    return len(content) > 0

def checkpoint4(content: list[str]):
    return 'cat123' in content
    

def checkpoint5():
    try:
        response = requests.get('http://localhost:5000/events')
        return "Enterprise-wide user-facing open architecture" in response.text
    except:
        return False

def calculate_total_score():
    scores = {
        checkpoint1: 1,
        checkpoint2: 1,
        checkpoint3: 1,
        checkpoint4: 1,
        checkpoint5: 4,
    }

    total_score = 0

    # Check RocketChat messages
    emily_msgs = get_history(username='emily_zhou')
    print(emily_msgs)
    zhang_msgs = get_history(username='zhang_wei')
    print(zhang_msgs)
    for func, score in scores.items():
        if func == checkpoint5:
            if func():
                total_score += score
        elif func == checkpoint1 or func == checkpoint2:
            if func(emily_msgs):
                total_score += score
        elif func == checkpoint3 or func == checkpoint4:
            if func(zhang_msgs):
                total_score += score
        else:
            raise ValueError(f"Unknown checkpoint: {func}")

    return total_score

# Compute the total points
total = calculate_total_score()
print(f"\nTotal points: {total}")
