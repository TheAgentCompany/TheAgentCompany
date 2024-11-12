import logging

from common import *
from scoring import Result, Checkpoint
from typing import List

rocket = create_rocketchat_client()
 

@grader
def grade_checkpoint1():
    return bool(get_rocketchat_personal_chat_history(rocket, 'huang_jie'))

@grader
def grade_checkpoint2():
    msgs = get_rocketchat_personal_chat_history(rocket, 'huang_jie')
    for msg in msgs:
        if '303' in msg:
            logging.info(f"Found correct answer in message: {msg}")
            return True
    
    logging.warning("No correct answer found in the conversation history")
    return False


def grade_checkpoints(trajectory=''):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    return result

