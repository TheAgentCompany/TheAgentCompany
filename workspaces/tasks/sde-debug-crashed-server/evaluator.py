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
    print(f"{users_list=}")
    for item in users_list:
        if item['username'] == username:
            id = item["_id"]
            break
    if id is None:
        raise ValueError("Could not find the user id for the AI agent.")
    im_history = rocket.im_history(room_id=id).json()
    print(f"{id=} {im_history=}")
    msgs = im_history.get('messages', [])
    for msg in msgs[::-1]:
        print(f"{username}'s chat: {msg['msg']}")
    return msgs

def checkpoint1(content: str):
    return 'emily' in content.lower()

def checkpoint2(content: str):
    return '2039fome' in content

def checkpoint3(content: str):
    return 'zhang' in content.lower()

def checkpoint4(content: str):
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
    msgs = get_history(username='jobbench')  # Assuming the AI agent's username is 'jobbench'
    content = ""
    for msg in msgs[::-1]:
        content += msg['msg'].lower()

    for func, score in scores.items():
        if func == checkpoint5:
            if func():
                total_score += score
        elif func(content):
            total_score += score

    return total_score

# Compute the total points
total = calculate_total_score()
print(f"\nTotal points: {total}")
