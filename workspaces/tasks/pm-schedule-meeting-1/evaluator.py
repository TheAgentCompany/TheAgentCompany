import os
from rocketchat_API.rocketchat import RocketChat

import datetime

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
    for msg in msgs:
        print(msg['msg'])

    if len(msgs)>0:
        return True
    else:
        return False

def check_thursday(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return False

    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().lower()

    # Check if "thursday" is in the file content
    if "thursday" in content:
        print("thursday is mentioned in the file.")
        return True
    else:
        print("thursday is not mentioned in the file.")
        return False

def checkpoint1(username='emily_zhou'):
    return get_history(username=username)

def checkpoint2(username='liu_qiang'):
    return get_history(username=username)

def checkpoint3(file_path = '/workspace/conclusion.txt'):
    return check_thursday(file_path=file_path)


def calculate_total_score():
    # 定义每个函数True时对应的分数
    scores = {
        checkpoint1: 1,
        checkpoint2: 2,
        checkpoint3: 3
    }

    total_score = 0

    for func, score in scores.items():
        if func():
            total_score += score

    return total_score

# compute the total point
total = calculate_total_score()
print(f"total point is: {total}")

