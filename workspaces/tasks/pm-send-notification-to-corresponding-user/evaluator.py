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
    for item in rocket.users_list().json()['users']:
        if item['username'] == username:
            id = item["_id"]
            break
    msgs = rocket.im_history(room_id=id).json()['messages']
    for msg in msgs[::-1]:
        print(f"{username}'s chat: {msg['msg']}")

    return msgs

def check_with_llm(msgs, pattern):
    content = ""
    for msg in msgs[::-1]:
        content += msg['msg']

    if len(content)==0:
        return False

    messages = [
        {
            "content": f"Does the text \"{content}\" include the plan to hold a kickoff meeting for the main Q4 project? Answer 'yes' if it does, or 'no' if it doesn't. Don't answer anything else.",
            "role": "user"}
    ]
    llm_resonse = llm_evaluator(messages).json()
    print(llm_resonse)

    if pattern in llm_resonse['choices'][0]['message']['content'].lower():
        return True
    else:
        return False

def checkpoint1(username='jessica_lee'):
    msgs = get_history(username=username)
    return check_with_llm(msgs, pattern='yes')

def checkpoint2(username='david_wong'):
    msgs = get_history(username=username)
    return check_with_llm(msgs, pattern='yes')

def checkpoint3(username='huang_jie'):
    msgs = get_history(username=username)
    return check_with_llm(msgs, pattern='yes')

def checkpoint4(username='mark_johnson'):
    msgs = get_history(username=username)
    return check_with_llm(msgs, pattern='yes')


def calculate_total_score():
    # Define the scores corresponding to when each function is True
    scores = {
        checkpoint1: 1,
        checkpoint2: 1,
        checkpoint3: 1,
        checkpoint4: 1,

    }

    total_score = 0

    for func, score in scores.items():
        if func():
            total_score += score

    return total_score

# compute the total point
total = calculate_total_score()
print(f"\ntotal point is: {total}")

