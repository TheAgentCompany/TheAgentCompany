import json
import logging

from common import *
from scoring import Result, Checkpoint, bonus_for_completing_final
from typing import List

rocket = create_rocketchat_client()
 

def checkpoint1():
    passed = True
    for name in ['jessica_lee', 'huang_jie', 'chen_xinyi']:
        passed = passed and bool(get_chat_history(rocket, name))
    return passed

def checkpoint2(trajectory):
    return "apps/files/files/1351?dir=/Documents/Administrative%20Specialist" in trajectory

def checkpoint3():
    """
    Jessica Lee: five Ergonomic Office Chair (Herman Miller) cost $1,195 each, five Standing Desk (Electric Adjustable) cost $649 each, three Meeting Table cost $899 each, total cost 1195*5+649*5+899*3=11917
    Huang Jie: three Desktop Computer (HP WorkStation) cost $1,499 each, three Wireless Mouse cost $69 each, three Wireless Keyboard cost $99 each, total cost 1499*3+69*3+99*3=5001
    Chen Xinyi: ten Laptop (Dell XPS 15) cost $1,799 each, ten Monitor Stand cost $79 each, total cost 1799*10+79*10=18780
    """
    consume_dict = {
        'jessica_lee': 11917,
        'huang_jie': 5001,
        'chen_xinyi': 18780
    }
    for key, value in consume_dict.items():
        chat_history = get_chat_history(rocket, key)
        if not any(str(value) in chat for chat in chat_history):
              return False
    return True


def grade_checkpoints(trajectory=''):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed1 = checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = checkpoint2(trajectory)
    checkpoints.append(Checkpoint(1, 1 * int(passed2)))

    passed3 = checkpoint3()
    checkpoints.append(Checkpoint(2, 2 * int(passed3)))

    return result
