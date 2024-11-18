
from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client, grader, get_rocketchat_personal_chat_history

# Create RocketChat instance
rocket = create_rocketchat_client()

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

    msgs = get_rocketchat_personal_chat_history(rocket, username='Chen Xinyi', content_only=True)
    content = ""
    for msg in msgs[::-1]:
        content += msg.lower() 

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func(content))))

    return result



