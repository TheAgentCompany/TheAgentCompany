import os
from rocketchat_API.rocketchat import RocketChat

import datetime

from llm_evaluator import *

# Set environment variables
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'ogma.lti.cs.cmu.edu'
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
    tmp = rocket.users_list().json()['users']
    for item in rocket.users_list().json()['users']:
        if item['username'] == username:
            id = item["_id"]
            break
    msgs = rocket.im_history(room_id=id).json()['messages']
    for msg in msgs[::-1]:
        print(f"{username}'s chat: {msg['msg']}")

    if len(msgs)>0:
        return True
    else:
        return False

def check_final_result(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return False

    # Read the content of the file and call litellm
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        messages = [{"content": f"Does the phrase \"\"{content}\"\" include Friday? Please answer 'yes' if it does, or 'no' if it doesn't.", "role": "user"}]

    # Check result
    llm_resonse = llm_evaluator(messages).json()
    print(llm_resonse)

    if 'yes' in llm_resonse['choices'][0]['message']['content'].lower():
        print("there is a meeting in this week")
        return True
    else:
        print("there is not a meeting in this week")
        return False

def checkpoint1(username='emily_zhou'):
    return get_history(username=username)

def checkpoint2(username='liu_qiang'):
    return get_history(username=username)

def checkpoint3(file_path = '/workspace/conclusion.txt'):
    return check_final_result(file_path=file_path)


def calculate_total_score():
    # Define the scores corresponding to when each function is True
    scores = {
        checkpoint1: 1,
        checkpoint2: 1,
        checkpoint3: 3
    }

    total_score = 0

    for func, score in scores.items():
        if func():
            total_score += score

    return total_score

# compute the total point
total = calculate_total_score()
print(f"\ntotal point is: {total}")

