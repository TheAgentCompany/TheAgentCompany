import logging

from typing import List

from scoring import Result, Checkpoint

from common import create_rocketchat_client
from common import evaluate_chat_history_with_llm
from common import get_rocketchat_personal_chat_history, checkpoint

# Initialize RocketChat client
rocket = create_rocketchat_client()

@grader
def grade_checkpoint_1():
    messages = get_rocketchat_personal_chat_history(rocket, 'Chen Xinyi')
    if not messages:
        logging.warning(f"No chat history found for Chen Xinyi")
        return False

    messages_cleaned = str(messages).lower()
    return 'green card' in messages_cleaned or 'citizen' in messages_cleaned


@grader
def grade_checkpoint_2():
    return evaluate_chat_history_with_llm(
        rocket,
        'Li Ming',
        'Jane Lee cannot be hired because she fails to meet visa/green card/citizenship requirement'
        )


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    checkpoints.append(Checkpoint(1, int(grade_checkpoint_1())))
    checkpoints.append(Checkpoint(2, 2 * int(grade_checkpoint_2())))
    return result



