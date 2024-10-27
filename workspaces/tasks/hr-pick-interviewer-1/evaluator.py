import requests
import logging
import os
import sys
import json
from typing import List
from scoring import Result, Checkpoint
from rocketchat_API.rocketchat import RocketChat  # type: ignore
from common import create_rocketchat_client, evaluate_with_llm, get_chat_history


LEADER_NAME = "Chen Xinyi"
TARGET_INTERVIEWER = "Emily Zhou"

# Create RocketChat instance
rocket = create_rocketchat_client()


def grade_checkpoint1():
    # [2pts] Check the chat history with the leader Chen Xinyi
    try:
        messages = get_chat_history(rocket, LEADER_NAME)
        composed_messages = compose_messages(messages)
        chat_with_leader = evaluate_with_llm(
            content=composed_messages,
            predicate=f"the examinee has a chat with the leader {LEADER_NAME} on the interviewer (there could be some irrelevant messages, but if could can find any message that is related to the interviewer, it should be considered as a chat)",
            additional_prompt="",
        )

        if not chat_with_leader:
            logging.error(f"There is no direct message with leader {LEADER_NAME}")
            return False
        return True
    except Exception as e:
        logging.error(f"Error fetching message data or evaluating: {e}")
        return False


def grade_checkpoint2():
    # [2pts] Check whether examinee chat with Emily Zhou (the right person).
    try:
        messages = get_chat_history(rocket, TARGET_INTERVIEWER)
        composed_messages = compose_messages(messages)
        chat_with_interviewer = evaluate_with_llm(
            content=composed_messages,
            predicate=f"there is a chat on inquiring whether the someone is available for a technical interview",
            additional_prompt="",
        )

        if not chat_with_interviewer:
            logging.error(
                f"The hr does not send the right message to the potential interviewer {TARGET_INTERVIEWER}"
            )
            return False

    except Exception as e:
        logging.error(f"Error fetching message data: {e}")
        return False

    return True


def grade_checkpoint3():
    # [2pts] Check whether examinee does not chat with others (Mike Chen, Wang Fang, David Wong, Huang Jie)

    target_names = ["Mark Johnson", "Jessica Lee", "David Wong"]
    for name in target_names:
        try:
            messages = get_chat_history(rocket, name)
            composed_messages = compose_messages(messages)
            chat_with_other = evaluate_with_llm(
                content=composed_messages,
                predicate=f"there is a chat on inquiring whether the someone is available for a technical interview",
                additional_prompt="",
            )

            if chat_with_other:
                logging.error(
                    f"The examinee sent the message to {name} who is not a match"
                )
                return False

        except Exception as e:
            logging.error(f"Error fetching message data: {e}")
            return False

    return True


def compose_messages(messages):
    return "\n".join(f"Message {i+1}: {msg}" for i, msg in enumerate(messages))


def grade_checkpoints() -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(2, 2 * int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(2, 2 * int(passed2)))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(2, 2 * int(passed3)))

    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))
