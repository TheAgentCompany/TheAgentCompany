
from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client
from common import get_chat_history

# Initialize RocketChat client
rocket = create_rocketchat_client()

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    chat_history = get_chat_history(rocket, "Chen Xinyi")
    checkpoints.append(Checkpoint(1, int(len(chat_history) > 0)))

    chat_history = get_chat_history(rocket, "Sarah Johnson")
    checkpoints.append(Checkpoint(1, int(len(chat_history) > 0)))

    mentioned_price = "365" in ' '.join(chat_history)
    checkpoints.append(Checkpoint(1, int(mentioned_price)))

    return result
