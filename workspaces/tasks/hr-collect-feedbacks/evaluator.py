
from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client
from common import get_rocketchat_personal_chat_history
from common import evaluate_chat_history_with_llm
from common import checkpoint

# Initialize RocketChat client
rocket = create_rocketchat_client()

@checkpoint
def grade_checkpoint4():
    performance_evaluatee = "Liu Qiang"
    return evaluate_chat_history_with_llm(rocket, performance_evaluatee, "the person receiving the feedback had an average job performance")


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    npcs = ["Mike Chen", "Li Ming", "Zhang Wei"]

    for npc in npcs:
        chat_history = get_rocketchat_personal_chat_history(rocket, npc)
        checkpoints.append(Checkpoint(1, int(len(chat_history) > 0)))

    passed = grade_checkpoint4()
    checkpoints.append(Checkpoint(2, 2 * int(passed)))

    return result


