import logging
import json
from typing import List
from scoring import Result, Checkpoint
from common import create_rocketchat_client, evaluate_chat_history_with_llm


LEADER_NAME = "Chen Xinyi"
TARGET_INTERVIEWER = "Emily Zhou"

# Create RocketChat instance
rocket = create_rocketchat_client()


def grade_checkpoint1():
    # [2pts] Check the chat history with the leader Chen Xinyi
    try:
        chat_with_leader = evaluate_chat_history_with_llm(
            rocket_client=rocket,
            username=LEADER_NAME,
            predicate="the examinee has a chat with the leader {LEADER_NAME} on the available interviewer list (there could be some irrelevant messages, but if could can find any message that is related to the interviewer, it should be considered as a chat)",
        )

        if not chat_with_leader:
            logging.error(f"There is no direct message with leader {LEADER_NAME}")
            return False
        return True
    except Exception as e:
        logging.error(f"Error fetching message data or evaluating: {e}")
        return False


def grade_checkpoint2():
    # [2pts] Check whether examinee chat with everyone (Emily Zhou, Mark Johnson, Jessica Lee, David Wong) on the availability.

    target_names = ["Emily Zhou", "Mark Johnson", "Jessica Lee", "David Wong"]
    for name in target_names:
        try:
            chat_with_other = evaluate_chat_history_with_llm(
                rocket_client=rocket,
                username=name,
                predicate="there is a conversation about whether someone is available for a technical interview",
            )

            if not chat_with_other:
                logging.error(f"The examinee did not send the message to {name}")
                return False

        except Exception as e:
            logging.error(f"Error fetching message data: {e}")
            return False

    return True


def grade_checkpoint3():
    # [2pts] Check whether the correct name (Emily Zhou) has been written to the interviewer.txt.

    try:
        with open("/workspace/interviewer.txt", "r") as f:
            content = f.read()
            if "Emily Zhou" in content:
                return True
            else:
                logging.error("Emily Zhou is not written to interviewer.txt")
                return False
    except Exception as e:
        logging.error(f"Error fetching message data: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
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
    print(grade_checkpoints())
