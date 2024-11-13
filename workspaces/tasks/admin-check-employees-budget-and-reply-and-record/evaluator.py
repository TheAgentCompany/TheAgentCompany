import logging
from common import *
from scoring import Result, Checkpoint, bonus_for_completing_final

from typing import List

rocket = create_rocketchat_client()


@grader
def grade_checkpoint1():
    passed = True
    for name in ['li_ming', 'zhang_wei', 'huang_jie', 'sophia_rodriguez']:
        passed = passed and bool(get_rocketchat_personal_chat_history(rocket, name))
    return passed


@grader
def grade_checkpoint2(trajectory):
    return "dir=/Documents/Administrative%20Specialist" in trajectory


@grader
def grade_checkpoint3():
    """
    Database:
        Li Ming:
            five Ergonomic Office Chair (Herman Miller) cost $1,195 each,
            five Standing Desk (Electric Adjustable) cost $649 each,
        Zhang Wei:
            three Meeting Table cost $899 each,
    total cost 1195*5+649*5+899*3=11917

    Product:
        Huang Jie:
            three Desktop Computer (HP WorkStation) cost $1,499 each,
            three Wireless Mouse cost $69 each,
        Sophia Rodriguez:
             three Wireless Keyboard cost $99 each,
    total cost 1499*3+69*3+99*3=5001

    """
    consume_dict = {'Li Ming': 9220, 'Zhang Wei': 2697, 'Huang Jie': 4704, 'Sophia Rodriguez': 297}

    for key, value in consume_dict.items():
        chat_history = get_rocketchat_personal_chat_history(rocket, key)
        if not any(str(value) in chat for chat in chat_history):
            return False
    return True


@grader
def grade_checkpoint4(file_path):
    """
    Database:
    total cost 1195*5+649*5+899*3=11917
    can remove two Meeting Table and one Standing Desk (Electric Adjustable), than total cost 1195*5+649*4+899*1=9470


    Product:
    total cost 1499*3+69*3+99*3=5001
    can remove one Wireless Keyboard, than total cost 1499*3+69*2+99*3=4932

    """
    if not file_path:
        return False

    try:
        with open(file_path, 'r') as f:
            content = f.read()

    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        return False

    return evaluate_with_llm(
        content=content,
        predicate='remove two Meeting Tables, remove one Standing Desk (Electric Adjustable), remove one Wireless Keyboard',
        additional_prompt='')


def grade_checkpoints(trajectory=''):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = grade_checkpoint2(trajectory)
    checkpoints.append(Checkpoint(1, 1 * int(passed2)))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(2, 2 * int(passed3)))

    passed4 = grade_checkpoint4(file_path='result.txt')
    checkpoints.append(Checkpoint(2, 2 * int(passed4)))

    return result
