import json
from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client

# Create RocketChat instance
rocket = create_rocketchat_client()

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

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    scores = {
        checkpoint1: 1,
        checkpoint2: 1,
        checkpoint3: 1,
    }

    msgs = get_history(username='chen_xinyi')
    content = ""
    for msg in msgs[::-1]:
        content += msg['msg'].lower()

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func(content))))

    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))
