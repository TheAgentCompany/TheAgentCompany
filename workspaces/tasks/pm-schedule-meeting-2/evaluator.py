import os
import logging

from common import evaluate_with_llm
from common import create_rocketchat_client

# Create RocketChat instance
rocket = create_rocketchat_client()


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

    if len(content) == 0:
        logging.warning("there is no content in the txt")
        return False

    predicate = 'the meeting is scheduled on Friday'
    additional_prompt = 'If meeting is not mentioned, but Friday is mentioned, that is fine'
    return evaluate_with_llm(content, predicate, additional_prompt)


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

