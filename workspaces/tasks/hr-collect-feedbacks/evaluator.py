import json
from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client
from common import get_chat_history
from common import evaluate_chat_history_with_llm

# Initialize RocketChat client
rocket = create_rocketchat_client()

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    npcs = ["Mike Chen", "Li Ming", "Zhang Wei"]
    performance_evaluatee = "Liu Qiang"

    for npc in npcs:
        chat_history = get_chat_history(rocket, npc)
        checkpoints.append(Checkpoint(1, int(len(chat_history) > 0)))

    passed = evaluate_chat_history_with_llm(rocket, performance_evaluatee, "the person receiving the feedback had an average job performance")
    checkpoints.append(Checkpoint(2, 2 * int(passed)))

    return result

if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))
