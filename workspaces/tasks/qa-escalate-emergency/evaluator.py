import logging
from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client, get_chat_history


SDE_NAME = "Zhang Wei"
CTO_NAME = "Sarah Johnson"

# Create RocketChat instance
rocket = create_rocketchat_client()


def grade_checkpoint1():
    return bool(get_chat_history(rocket, SDE_NAME))


def grade_checkpoint2():
    return bool(get_chat_history(rocket, CTO_NAME))

def grade_checkpoint3():
    chat_with_sde = get_chat_history(rocket, SDE_NAME, content_only=False)
    chat_with_cto = get_chat_history(rocket, CTO_NAME, content_only=False)
    # check whether the first message sent to CTO is at least 10 minutes after the first message sent to SDE
    logging.info(f"First message sent to SDE: {chat_with_sde[0]['ts']}")
    logging.info(f"First message sent to CTO: {chat_with_cto[0]['ts']}")
    time_diff = chat_with_cto[0]['ts'] - chat_with_sde[0]['ts']
    logging.info(f"Time difference: {time_diff}")
    return chat_with_cto and time_diff > 600


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = passed1 and grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = passed1 and passed2 and grade_checkpoint3()
    checkpoints.append(Checkpoint(1, int(passed3)))

    return result
