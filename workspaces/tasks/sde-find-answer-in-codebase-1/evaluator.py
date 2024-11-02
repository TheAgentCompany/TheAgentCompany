import logging
import json
from typing import List
from scoring import Result, Checkpoint
from common import create_rocketchat_client, evaluate_chat_history_with_llm


# Create RocketChat instance
rocket = create_rocketchat_client()


def grade_checkpoint1():
    # [3pts] Check if the correct PR number (#8676) in `llama.cpp` (http://the-agent-company.com:8929/root/llama.cpp) exists in the chat with Chen Xinyi.

    try:
        get_correct_pr = evaluate_chat_history_with_llm(
            rocket_client=rocket,
            username="Chen Xinyi",
            predicate="the chat history mentions PR number 8676",
        )

        if not get_correct_pr:
            logging.error(f"The examinee does not mention the correct PR number")
            return False
        return True
    except Exception as e:
        logging.error(f"Error fetching message data or evaluating: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(3, 3 * int(passed1)))

    return result
