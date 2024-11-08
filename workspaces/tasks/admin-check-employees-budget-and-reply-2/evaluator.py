
from common import *
from scoring import Result, Checkpoint, bonus_for_completing_final

from typing import List

rocket = create_rocketchat_client()
 

def checkpoint1():
    passed = True
    for name in ['mike_chen', 'huang_jie', 'chen_xinyi', 'sophia_rodriguez']:
        passed = passed and bool(get_rocketchat_personal_chat_history(rocket, name))
    return passed

def checkpoint2(trajectory):
    return "dir=/Documents/Administrative%20Specialist" in trajectory

def checkpoint3():
    """
    sophia_rodriguez: $69+$99
    huang_jie: $899
    mike_chen:  $1,799
    """
    balance_dict = {
        'sophia_rodriguez': 168,
        'huang_jie': 899,
        'mike_chen': 1799
    }
    for key, value in balance_dict.items():
        is_value = evaluate_chat_history_with_llm(rocket, key, value)
        if not is_value:
              return False

    state_dict = {
        'Sophia Rodriguez': 'under budget',
        'Huang Jie': 'under budget',
        'Mike Chen': 'exceed budget'
    }
    for key, value in state_dict.items():
        is_value = evaluate_chat_history_with_llm(rocket, key, value)
        if not is_value:
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