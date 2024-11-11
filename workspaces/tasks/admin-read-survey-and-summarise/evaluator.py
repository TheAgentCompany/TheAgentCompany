
from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client, grader

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

@grader
def grade_checkpoint1(content: str):
    return content is not None and len(content) > 0

@grader
def grade_checkpoint2(content: str):
    if content is None or len(content) == 0:
        return False
    return 'coke' in content and 'dew' in content

@grader
def grade_checkpoint3(content: str):
    if content is None or len(content) == 0:
        return False
    return 'apple' in content and 'sprite' in content

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    scores = {
        grade_checkpoint1: 1,
        grade_checkpoint2: 1,
        grade_checkpoint3: 1,
    }

    msgs = get_history(username='chen_xinyi')
    content = ""
    for msg in msgs[::-1]:
        content += msg['msg'].lower()

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func(content))))

    return result



