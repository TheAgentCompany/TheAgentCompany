
from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client
from common import get_rocketchat_personal_chat_history
from common import evaluate_chat_history_with_llm

# Initialize RocketChat client
rocket = create_rocketchat_client()


def grade_checkpoint1(trajectory=""):
    return trajectory is not None and "/Documents/Human%20Resources%20Team/Immigration" in trajectory


def grade_checkpoint2():
    history = get_rocketchat_personal_chat_history(rocket, "Priya Sharma")
    return history is not None and "niw" in str(history).lower()


def grade_checkpoint3():
    return evaluate_chat_history_with_llm(rocket, "Priya Sharma", "the current date of filing is 01AUG23 (August 1st, 2023)")


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))

    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))

    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))

    return result
