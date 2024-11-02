import logging
import json
from typing import List
from scoring import Result, Checkpoint
from common import create_rocketchat_client, evaluate_chat_history_with_llm


# Create RocketChat instance
rocket = create_rocketchat_client()


def grade_checkpoint1():
    # [2pts] Check if the examinee chat with the correct person (Mike Chen)
    try:
        chat_with_target = evaluate_chat_history_with_llm(
            rocket_client=rocket,
            username="Mike Chen",
            predicate="there is a conversation about 'llama3.1 context size related code'",
        )

        if not chat_with_target:
            logging.error(
                f"the examinee does not ask Mike Chen on 'llama3.1 context size' related questions'"
            )
            return False
        return True
    except Exception as e:
        logging.error(f"Error fetching message data or evaluating: {e}")
        return False


def grade_checkpoint2():
    # [3pts] Check if the correct pr (#8676) exist in the `/workspace/solution.txt`.

    try:
        with open("/workspace/solution.txt", "r") as f:
            solution = f.read()
            if "8676" not in solution.lower():
                logging.error(
                    f"The correct pr number (8676) does not exist in the `/workspace/solution.txt`"
                )
                return False
            return True

    except Exception as e:
        logging.error(f"Error reading solution file: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    passed2 = grade_checkpoint2()

    checkpoints.append(Checkpoint(2, 2 * int(passed1)))
    checkpoints.append(Checkpoint(3, 3 * int(passed2)))

    return result
