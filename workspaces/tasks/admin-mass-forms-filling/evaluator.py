from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final

from common import create_rocketchat_client
from common import evaluate_chat_history_with_llm
from common import get_rocketchat_personal_chat_history
from common import grader

# Initialize RocketChat client
rocket = create_rocketchat_client()

@grader
def run_checkpoint_1(trajectory: str):
    # there are 94 resumes in resumes.zip
    return "94" in trajectory


@grader
def run_checkpoint_2():
    return bool(get_rocketchat_personal_chat_history(rocket, 'Chen Xinyi'))


@grader
def run_checkpoint_3():
    return bool(evaluate_chat_history_with_llm(
        rocket,
        'Chen Xinyi',
        'Alex Chen is the only qualified candidate'
    ))


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)
    checkpoints.append(Checkpoint(1, int(run_checkpoint_1(trajectory))))
    checkpoints.append(Checkpoint(1, int(run_checkpoint_2())))
    checkpoints.append(Checkpoint(3, 3 * int(run_checkpoint_3())))
    return result
