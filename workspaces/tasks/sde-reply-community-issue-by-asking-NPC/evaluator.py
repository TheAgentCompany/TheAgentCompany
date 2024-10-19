import os
import sys
import requests
from rocketchat_API.rocketchat import RocketChat
import urllib.parse
import logging

from llm_evaluator import *

# Configuration for rocketchat
SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'ogma.lti.cs.cmu.edu'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASSWORD = 'jobbench'

rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASSWORD, server_url=ROCKETCHAT_URL)

# Configuration for gitlab
base_url = "http://the-agent-company.com:8929/api/v4"
project_path = "root/openhands"
issue_id = 4158
access_token = "root-token"
headers = {"PRIVATE-TOKEN": access_token}


def get_gitlab_issue_notes():
    encoded_path = urllib.parse.quote(project_path, safe='')
    url = f"{base_url}/projects/{encoded_path}/issues/{issue_id}/notes"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        logging.error(f"Error occurred while checking the repository: {e}")
        return {}

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


def check_with_llm(msgs, target, expect_result):
    content = ""
    for msg in msgs[::-1]:
        content += msg['msg']

    if len(content) == 0:
        return False
    messages = [
        {
            "content": f"Does the text \"{content}\" means the \"{target}\"? Answer 'yes' if it does, or 'no' if it doesn't. Don't answer anything else.",
            "role": "user"}
    ]
    llm_resonse = llm_evaluator(messages).json()

    if expect_result in llm_resonse['choices'][0]['message']['content'].lower():
        return True
    else:
        return False


def checkpoint1(url='http://the-agent-company.com:8929/root/openhands/-/issues/4158'):
    if len(sys.argv) < 2:
        trajectory = ""
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                trajectory = file.read()
        except Exception as e:
            print(f"Error reading trajectory file: {e}")
            exit(1)
    return url in trajectory


def checkpoint2(username='mike_chen'):
    msgs = get_history(username=username)
    return bool(msgs)


def checkpoint3():
    issue_notes = get_gitlab_issue_notes()
    if issue_notes:
        return any(issue_note.get('id') not in [127283, 127284, 127285] for issue_note in issue_notes)
    else:
        return False

def checkpoint4(username='mike_chen'):
    msgs = get_history(username=username)

    issue_notes = get_gitlab_issue_notes()
    if issue_notes:
        for issue_note in issue_notes:
            if issue_note.get('id') not in [127283, 127284, 127285]:
                target = issue_note.get('body')
    else:
        return False

    return check_with_llm(
        msgs=msgs,
        target=target,
        expect_result='yes'
    )

def calculate_total_score():
    # Define the scores corresponding to when each function is True
    scores = {
        checkpoint1: 1,
        checkpoint2: 1,
        checkpoint3: 1,
        checkpoint4: 2,

    }

    total_score = 0

    for func, score in scores.items():
        if func():
            total_score += score

    return total_score

# compute the total point
total = calculate_total_score()
print(f"\ntotal point is: {total}")
